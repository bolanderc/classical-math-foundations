param(
    [string]$Python = "python",
    [string]$Voice = "en-NZ-MollyNeural",
    [double]$PlaybackSpeed = 0.75
)

$ErrorActionPreference = "Stop"

$projectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$sceneFile = Join-Path $PSScriptRoot "proposition1.py"
$narrationFile = Join-Path $PSScriptRoot "proposition1-narration.txt"
$mediaDir = Join-Path $projectRoot "media"
$audioFile = Join-Path $mediaDir "proposition1-narration.mp3"
$subtitleFile = Join-Path $mediaDir "proposition1-narration.srt"
$silentVideo = Join-Path $mediaDir "videos\proposition1\720p30\proposition1-silent.mp4"
$outputVideo = Join-Path $projectRoot "book1\figures\proposition1.mp4"

$ffmpegCommand = Get-Command ffmpeg -ErrorAction SilentlyContinue
if ($ffmpegCommand) {
    $ffmpeg = $ffmpegCommand.Source
}
else {
    $bundledFfmpeg = (& $Python -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())").Trim()
    $ffmpegDir = Join-Path $mediaDir ".tools"
    $ffmpeg = Join-Path $ffmpegDir "ffmpeg.exe"
    New-Item -ItemType Directory -Force -Path $ffmpegDir | Out-Null
    Copy-Item -Force $bundledFfmpeg $ffmpeg
    $env:PATH = "$ffmpegDir;$env:PATH"
}

& $Python -m manim -qm --disable_caching $sceneFile EuclidPropositionOne `
    -o "proposition1-silent.mp4" --media_dir $mediaDir
if ($LASTEXITCODE -ne 0) {
    throw "Manim failed with exit code $LASTEXITCODE."
}

if ($PlaybackSpeed -le 0) {
    throw "PlaybackSpeed must be greater than zero."
}

$speechRate = [math]::Round(($PlaybackSpeed - 1) * 100)
$rateArgument = if ($speechRate -ge 0) { "+$speechRate%" } else { "$speechRate%" }
& $Python -m edge_tts --file $narrationFile --voice $Voice `
    --rate=$rateArgument --write-media $audioFile --write-subtitles $subtitleFile
if ($LASTEXITCODE -ne 0) {
    throw "Neural narration failed with exit code $LASTEXITCODE. Check the internet connection and voice name."
}

$videoRate = 1 / $PlaybackSpeed
$videoFilter = "setpts=$videoRate*PTS,fps=30,tpad=stop_mode=clone:stop_duration=10"
$lastCue = Select-String -Path $subtitleFile -Pattern '--> (\d{2}):(\d{2}):(\d{2}),(\d{3})' | Select-Object -Last 1
if (-not $lastCue) {
    throw "Could not determine the narration duration from $subtitleFile."
}
$cueMatch = $lastCue.Matches[0]
$narrationDuration = (
    [int]$cueMatch.Groups[1].Value * 3600 +
    [int]$cueMatch.Groups[2].Value * 60 +
    [int]$cueMatch.Groups[3].Value +
    [int]$cueMatch.Groups[4].Value / 1000
)
$sceneDuration = 31.35
$slowedVideoDuration = $sceneDuration / $PlaybackSpeed
$outputDuration = [math]::Max($slowedVideoDuration + 0.75, $narrationDuration + 0.75)
& $ffmpeg -y -i $silentVideo -i $audioFile -filter_complex "[0:v]$videoFilter[v]" `
    -map "[v]" -map "1:a:0" -c:v libx264 -preset medium -crf 20 `
    -c:a aac -b:a 96k -t $outputDuration -movflags +faststart $outputVideo
if ($LASTEXITCODE -ne 0) {
    throw "FFmpeg failed with exit code $LASTEXITCODE."
}

Write-Host "Narrated animation written to $outputVideo using $Voice at $PlaybackSpeed speed."

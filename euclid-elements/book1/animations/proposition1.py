"""Manim scene for Euclid, Elements, Book I, Proposition 1.

Render the narrated version from the ``euclid-elements`` directory with:

    powershell -ExecutionPolicy Bypass -File \
        book1/animations/render_proposition1.ps1
"""

from manim import (
    BLUE,
    DOWN,
    FadeIn,
    FadeOut,
    GREEN,
    LEFT,
    ORIGIN,
    RIGHT,
    Scene,
    Text,
    UP,
    WHITE,
    YELLOW,
    Circle,
    Create,
    Dot,
    Line,
    VGroup,
    config,
)


config.background_color = "#111827"


class EuclidPropositionOne(Scene):
    """Construct an equilateral triangle on a given finite straight line."""

    def construct(self):
        title = Text(
            "Euclid · Book I · Proposition 1",
            font_size=38,
            color=WHITE,
        ).to_edge(UP, buff=0.35)
        subtitle = Text(
            "Construct an equilateral triangle on a given line segment",
            font_size=24,
            color="#CBD5E1",
        ).next_to(title, DOWN, buff=0.12)
        self.play(FadeIn(title, shift=DOWN), FadeIn(subtitle, shift=DOWN))
        self.wait(2.6)

        a = LEFT * 1.8 + DOWN * 1.5
        b = RIGHT * 1.8 + DOWN * 1.5
        radius = 3.6
        c = ORIGIN + UP * (radius * 3**0.5 / 2 - 1.5)

        point_a = Dot(a, color=WHITE)
        point_b = Dot(b, color=WHITE)
        label_a = Text("A", font_size=28).next_to(point_a, DOWN + LEFT, buff=0.12)
        label_b = Text("B", font_size=28).next_to(point_b, DOWN + RIGHT, buff=0.12)
        base = Line(a, b, color=YELLOW, stroke_width=6)
        step = Text("1. Begin with the given segment AB", font_size=28, color=YELLOW)
        step.to_edge(DOWN, buff=0.35)

        self.play(Create(base), FadeIn(point_a), FadeIn(point_b))
        self.play(FadeIn(label_a), FadeIn(label_b), FadeIn(step))
        self.wait(0.8)

        circle_a = Circle(radius=radius, color=BLUE, stroke_width=4).move_to(a)
        step_two = Text(
            "2. Draw a circle centered at A with radius AB",
            font_size=28,
            color=BLUE,
        ).to_edge(DOWN, buff=0.35)
        self.play(FadeOut(step), Create(circle_a), FadeIn(step_two))
        self.wait(3.3)

        circle_b = Circle(radius=radius, color=GREEN, stroke_width=4).move_to(b)
        step_three = Text(
            "3. Draw a circle centered at B with the same radius",
            font_size=28,
            color=GREEN,
        ).to_edge(DOWN, buff=0.35)
        self.play(FadeOut(step_two), Create(circle_b), FadeIn(step_three))
        self.wait(3.5)

        point_c = Dot(c, color=WHITE)
        label_c = Text("C", font_size=28).next_to(point_c, UP, buff=0.12)
        step_four = Text(
            "4. Let C be an intersection of the circles",
            font_size=28,
            color=WHITE,
        ).to_edge(DOWN, buff=0.35)
        self.play(
            FadeOut(step_three),
            FadeIn(point_c, scale=1.6),
            FadeIn(label_c),
            FadeIn(step_four),
        )
        self.wait(1.75)

        side_ac = Line(a, c, color=YELLOW, stroke_width=6)
        side_bc = Line(b, c, color=YELLOW, stroke_width=6)
        join_step = Text(
            "5. Join A to C and B to C",
            font_size=28,
            color=YELLOW,
        ).to_edge(DOWN, buff=0.35)
        result = Text(
            "AB = AC = BC, so △ABC is equilateral",
            font_size=30,
            color=YELLOW,
        ).to_edge(DOWN, buff=0.35)
        self.play(FadeOut(step_four), Create(side_ac), Create(side_bc), FadeIn(join_step))
        self.wait(2.4)
        self.play(FadeOut(join_step), FadeIn(result))
        self.wait(2.5)

        triangle = VGroup(base, side_ac, side_bc)
        self.play(
            circle_a.animate.set_stroke(opacity=0.25),
            circle_b.animate.set_stroke(opacity=0.25),
            triangle.animate.set_stroke(width=8),
        )
        self.wait(5.5)

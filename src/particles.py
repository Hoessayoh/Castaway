import pygame
import random
import math


class Particle:
    """Single particle for effects"""

    def __init__(self, x, y, color, velocity, lifetime, size=3):
        self.x = x
        self.y = y
        self.color = color
        self.vx, self.vy = velocity
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.size = size
        self.gravity = 0.2
        self.alpha = 255

    def update(self):
        """Update particle position and lifetime"""
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity  # Apply gravity
        self.lifetime -= 1

        # Fade out
        self.alpha = int(255 * (self.lifetime / self.max_lifetime))

    def draw(self, screen):
        """Draw the particle"""
        if self.lifetime > 0:
            # Create surface with alpha
            surf = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
            color_with_alpha = (*self.color[:3], self.alpha)
            pygame.draw.circle(surf, color_with_alpha, (self.size, self.size), self.size)
            screen.blit(surf, (int(self.x - self.size), int(self.y - self.size)))

    def is_alive(self):
        """Check if particle is still alive"""
        return self.lifetime > 0


class ParticleSystem:
    """Manages all particle effects"""

    def __init__(self):
        self.particles = []

    def create_catch_explosion(self, x, y, rarity_color, is_shiny=False):
        """Create explosion effect when catching a fish"""
        particle_count = 30 if is_shiny else 20

        for i in range(particle_count):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(2, 6)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed - 2  # Bias upward

            # Use rarity color with some variation
            color_variation = random.randint(-30, 30)
            particle_color = (
                max(0, min(255, rarity_color[0] + color_variation)),
                max(0, min(255, rarity_color[1] + color_variation)),
                max(0, min(255, rarity_color[2] + color_variation))
            )

            lifetime = random.randint(30, 60)
            size = random.randint(2, 5)

            particle = Particle(x, y, particle_color, (vx, vy), lifetime, size)
            self.particles.append(particle)

        # Add some sparkles for shiny
        if is_shiny:
            for i in range(15):
                angle = random.uniform(0, math.pi * 2)
                speed = random.uniform(3, 8)
                vx = math.cos(angle) * speed
                vy = math.sin(angle) * speed - 3

                sparkle_color = (255, 255, random.randint(200, 255))
                lifetime = random.randint(40, 70)

                particle = Particle(x, y, sparkle_color, (vx, vy), lifetime, 4)
                self.particles.append(particle)

    def create_level_up_effect(self, x, y):
        """Create level up effect"""
        for i in range(40):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(2, 5)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed - 3

            # Golden particles
            color = (
                random.randint(200, 255),
                random.randint(180, 230),
                random.randint(0, 100)
            )

            lifetime = random.randint(40, 80)
            size = random.randint(3, 6)

            particle = Particle(x, y, color, (vx, vy), lifetime, size)
            self.particles.append(particle)

    def create_achievement_effect(self, x, y):
        """Create achievement unlock effect"""
        for i in range(50):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(3, 7)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed - 4

            # Purple/gold particles
            if random.random() < 0.5:
                color = (random.randint(150, 200), random.randint(50, 100), random.randint(200, 255))
            else:
                color = (255, random.randint(200, 230), 0)

            lifetime = random.randint(50, 90)
            size = random.randint(3, 7)

            particle = Particle(x, y, color, (vx, vy), lifetime, size)
            self.particles.append(particle)

    def create_water_splash(self, x, y):
        """Create water splash when casting"""
        for i in range(15):
            angle = random.uniform(-math.pi / 3, -2 * math.pi / 3)  # Upward arc
            speed = random.uniform(3, 6)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed

            # Water blue color
            color = (
                random.randint(70, 120),
                random.randint(140, 180),
                random.randint(200, 255)
            )

            lifetime = random.randint(20, 40)
            size = random.randint(2, 4)

            particle = Particle(x, y, color, (vx, vy), lifetime, size)
            self.particles.append(particle)

    def create_bobber_ripple(self, x, y):
        """Create small ripple around bobber"""
        for i in range(5):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(0.5, 1.5)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed * 0.3  # Flatter

            color = (100, 150, 200)
            lifetime = random.randint(15, 30)
            size = 2

            particle = Particle(x, y, color, (vx, vy), lifetime, size)
            self.particles.append(particle)

    def create_stars(self, x, y, count=5):
        """Create star particles (for special catches)"""
        for i in range(count):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(1, 3)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed - 2

            color = (255, 255, random.randint(150, 255))
            lifetime = random.randint(40, 60)
            size = random.randint(4, 6)

            particle = Particle(x, y, color, (vx, vy), lifetime, size)
            self.particles.append(particle)

    def update(self):
        """Update all particles"""
        for particle in self.particles:
            particle.update()

        # Remove dead particles
        self.particles = [p for p in self.particles if p.is_alive()]

    def draw(self, screen):
        """Draw all particles"""
        for particle in self.particles:
            particle.draw(screen)

    def clear(self):
        """Clear all particles"""
        self.particles.clear()


class FloatingText:
    """Floating text effect (for damage numbers, etc.)"""

    def __init__(self, x, y, text, color, duration=60, rise_speed=1):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.duration = duration
        self.max_duration = duration
        self.rise_speed = rise_speed
        self.alpha = 255
        self.font = pygame.font.Font(None, 36)

    def update(self):
        """Update position and lifetime"""
        self.y -= self.rise_speed
        self.duration -= 1
        self.alpha = int(255 * (self.duration / self.max_duration))

    def draw(self, screen):
        """Draw the floating text"""
        if self.duration > 0:
            # Render text with outline
            text_surf = self.font.render(self.text, True, self.color)

            # Create surface with alpha
            alpha_surf = pygame.Surface(text_surf.get_size(), pygame.SRCALPHA)
            alpha_surf.blit(text_surf, (0, 0))
            alpha_surf.set_alpha(self.alpha)

            # Draw outline
            outline_surf = self.font.render(self.text, True, (0, 0, 0))
            for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                outline_alpha = pygame.Surface(outline_surf.get_size(), pygame.SRCALPHA)
                outline_alpha.blit(outline_surf, (0, 0))
                outline_alpha.set_alpha(self.alpha)
                screen.blit(outline_alpha, (int(self.x + dx), int(self.y + dy)))

            screen.blit(alpha_surf, (int(self.x), int(self.y)))

    def is_alive(self):
        """Check if text is still visible"""
        return self.duration > 0


class FloatingTextSystem:
    """Manages floating text effects"""

    def __init__(self):
        self.texts = []

    def add_text(self, x, y, text, color, duration=60, rise_speed=1):
        """Add a new floating text"""
        floating_text = FloatingText(x, y, text, color, duration, rise_speed)
        self.texts.append(floating_text)

    def add_exp_text(self, x, y, exp_amount):
        """Add EXP gain text"""
        self.add_text(x, y, f"+{exp_amount} EXP", (144, 238, 144), 80, 1.5)

    def add_gold_text(self, x, y, gold_amount):
        """Add gold gain text"""
        self.add_text(x, y, f"+{gold_amount}g", (255, 215, 0), 80, 1.5)

    def update(self):
        """Update all floating texts"""
        for text in self.texts:
            text.update()

        # Remove dead texts
        self.texts = [t for t in self.texts if t.is_alive()]

    def draw(self, screen):
        """Draw all floating texts"""
        for text in self.texts:
            text.draw(screen)

    def clear(self):
        """Clear all texts"""
        self.texts.clear()

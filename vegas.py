import argparse
import time
import rich
import pygame
import math

from random import randint as random_integer
from rich import print as rprint
from rich.console import Console
from rich.status import Status

def is_odd(number: int) -> bool:
     return number % 2 == 1

def is_even(number: int) -> bool:
     return number % 2 == 0

pygame.mixer.init()  
spin_sound = pygame.mixer.Sound("Roulette_Ball.mp3")

pygame.init()
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Vegas Roulette")
clock = pygame.time.Clock()

def get_number_color(num, index):
    if num == 0:
        return (0, 128, 0)
    elif index % 2 == 1:
        return (0, 0, 0)
    else:
        return (200, 0, 0)

ROULETTE_NUMBERS = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26]

def draw_roulette_wheel(rotation_angle, ball_angle, target_number=None):
    """Draw the roulette wheel with rotation and ball position"""
    screen.fill((34, 139, 34))
    
    center_x, center_y = WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2
    outer_radius = 250
    inner_radius = 100
    
    # Draw outer wheel
    pygame.draw.circle(screen, (139, 69, 19), (center_x, center_y), outer_radius, 5)
    
    # Draw number slots
    num_slots = len(ROULETTE_NUMBERS)
    angle_per_slot = 2 * math.pi / num_slots
    
    for i, num in enumerate(ROULETTE_NUMBERS):
        angle = i * angle_per_slot + rotation_angle
        start_angle = angle
        end_angle = angle + angle_per_slot
        
        # Draw slot
        color = get_number_color(num, i)
        points = [
            (center_x, center_y),
            (center_x + outer_radius * math.cos(start_angle), center_y + outer_radius * math.sin(start_angle)),
            (center_x + outer_radius * math.cos(end_angle), center_y + outer_radius * math.sin(end_angle))
        ]
        pygame.draw.polygon(screen, color, points)
        pygame.draw.polygon(screen, (255, 255, 255), points, 2)
        
        # Draw number text
        text_angle = angle + angle_per_slot / 2
        text_radius = (outer_radius + inner_radius) / 2
        text_x = center_x + text_radius * math.cos(text_angle)
        text_y = center_y + text_radius * math.sin(text_angle)
        
        font = pygame.font.Font(None, 24)
        text = font.render(str(num), True, (255, 255, 255) if color == (0, 0, 0) else (255, 255, 255))
        text_rect = text.get_rect(center=(text_x, text_y))
        screen.blit(text, text_rect)
    
    # Draw center circle
    pygame.draw.circle(screen, (139, 69, 19), (center_x, center_y), inner_radius)
    pygame.draw.circle(screen, (255, 255, 255), (center_x, center_y), inner_radius, 3)
    
    # Draw ball
    ball_radius = 8
    ball_x = center_x + (outer_radius - 15) * math.cos(ball_angle + rotation_angle)
    ball_y = center_y + (outer_radius - 15) * math.sin(ball_angle + rotation_angle)
    pygame.draw.circle(screen, (255, 255, 255), (int(ball_x), int(ball_y)), ball_radius)
    pygame.draw.circle(screen, (200, 200, 200), (int(ball_x), int(ball_y)), ball_radius - 2)
    
    # Draw pointer at top
    pointer_points = [
        (center_x, center_y - outer_radius - 20),
        (center_x - 15, center_y - outer_radius - 5),
        (center_x + 15, center_y - outer_radius - 5)
    ]
    pygame.draw.polygon(screen, (255, 215, 0), pointer_points)
    
    # Highlight target number if provided
    if target_number is not None:
        try:
            target_idx = ROULETTE_NUMBERS.index(target_number)
            target_angle = target_idx * angle_per_slot + rotation_angle
            highlight_radius = outer_radius + 10
            highlight_x = center_x + highlight_radius * math.cos(target_angle + angle_per_slot / 2)
            highlight_y = center_y + highlight_radius * math.sin(target_angle + angle_per_slot / 2)
            pygame.draw.circle(screen, (255, 255, 0), (int(highlight_x), int(highlight_y)), 15, 3)
        except ValueError:
            pass
    
    pygame.display.flip()

def show_spinning_wheel(spin_time: float):
    spin_sound.play()
    
    start_time = time.time()
    initial_rotation = random_integer(0, 360) * math.pi / 180
    rotation_speed = 0.15
    ball_speed = 0.25
    
    rotation_angle = initial_rotation
    ball_angle = 0
    
    running = True
    pointer_angle = 3 * math.pi / 2
    
    while time.time() - start_time < spin_time and running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
        
        elapsed = time.time() - start_time
        progress = elapsed / spin_time
        
        if progress > 0.7:
            target_ball_angle = (pointer_angle - rotation_angle) % (2 * math.pi)
            if target_ball_angle < 0:
                target_ball_angle += 2 * math.pi
            
            final_phase_progress = (progress - 0.7) / 0.3
            ease_factor = 1 - (1 - final_phase_progress) ** 2
            
            angle_diff = (target_ball_angle - ball_angle) % (2 * math.pi)
            if angle_diff > math.pi:
                angle_diff -= 2 * math.pi
            
            ball_distance_to_target = abs(angle_diff)
            if ball_distance_to_target < 0.1:
                current_rotation_speed = 0
            else:
                wheel_slowdown = 1 - final_phase_progress * 0.98
                slowdown_factor = (1 - progress * 0.7) * wheel_slowdown
                current_rotation_speed = rotation_speed * slowdown_factor
            
            ball_angle = ball_angle + angle_diff * ease_factor
            ball_angle = ball_angle % (2 * math.pi)
            if ball_angle < 0:
                ball_angle += 2 * math.pi
        else:
            slowdown_factor = 1 - progress * 0.95
            current_rotation_speed = rotation_speed * slowdown_factor
            current_ball_speed = ball_speed * slowdown_factor
            ball_angle += current_ball_speed
        
        rotation_angle += current_rotation_speed
        draw_roulette_wheel(rotation_angle, ball_angle)
        clock.tick(60)
    
    center_x, center_y = WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2
    outer_radius = 250
    inner_radius = 100
    text_radius = (outer_radius + inner_radius) / 2
    
    num_slots = len(ROULETTE_NUMBERS)
    angle_per_slot = 2 * math.pi / num_slots

    pointer_target_x = center_x
    pointer_target_y = center_y - outer_radius

    min_distance = float('inf')
    slot_index = 0
    
    for i in range(num_slots):

        angle = i * angle_per_slot + rotation_angle
        text_angle = angle + angle_per_slot / 2
        
        text_x = center_x + text_radius * math.cos(text_angle)
        text_y = center_y + text_radius * math.sin(text_angle)
        
        distance = math.sqrt((pointer_target_x - text_x)**2 + (pointer_target_y - text_y)**2)
        
        if distance < min_distance:
            min_distance = distance
            slot_index = i
    
    winning_number = ROULETTE_NUMBERS[slot_index]
    
    pointer_angle = 3 * math.pi / 2
    target_ball_angle = (pointer_angle - rotation_angle) % (2 * math.pi)
    if target_ball_angle < 0:
        target_ball_angle += 2 * math.pi
    ball_angle = target_ball_angle
    

    for _ in range(30):
        draw_roulette_wheel(rotation_angle, ball_angle, winning_number)
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break
    
    return winning_number

def spin_wheel() -> int:
    my_num = random_integer(0,35)
    if my_num == 0:
        rprint(f"[bold green]{my_num}[/bold green]")
    elif is_odd(my_num):
        rprint(f"[bold black]{my_num}[/bold black]")
    elif is_even(my_num):
        rprint(f"[bold red]{my_num}[/bold red]")
    return my_num

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--num-spins", type=int, default=1, required=False)
    parser.add_argument("--spin-time", type=float, default=6.0, required=False)
    args = parser.parse_args()

    for _ in range(args.num_spins):
       
        result = show_spinning_wheel(args.spin_time)
   
        if result == 0:
            rprint(f"[bold green]{result}[/bold green]")
        elif is_odd(result):
            rprint(f"[bold black]{result}[/bold black]")
        elif is_even(result):
            rprint(f"[bold red]{result}[/bold red]")
    
    pygame.quit()
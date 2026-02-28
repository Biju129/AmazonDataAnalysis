import pygame
import serial
import time

# ---------- Arduino Serial ----------
arduino = serial.Serial('COM7' ,9600)
time.sleep(2)

def lcd(text):
    arduino.write((text + '\n').encode())

# ---------- Pygame ----------
pygame.init()
screen = pygame.display.set_mode((800, 500))
pygame.display.set_caption("MCQ Quiz Game")
font = pygame.font.SysFont(None, 32)
big_font = pygame.font.SysFont(None, 40)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100, 149, 237)
GREEN = (0, 200, 0)
RED = (200, 0, 0)

# ---------- Quiz Data ----------
quiz = [
    {
        "question": "India's national bird?",
        "options": ["Peacock", "Sparrow", "Eagle", "Parrot"],
        "answer": "Peacock"
    },
    {
        "question": "Capital of India?",
        "options": ["Mumbai", "New Delhi", "Kolkata", "Chennai"],
        "answer": "New Delhi"
    },
    {
        "question": "National animal?",
        "options": ["Lion", "Elephant", "Tiger", "Cheetah"],
        "answer": "Tiger"
    },
    {
        "question": "National flower?",
        "options": ["Lotus", "Rose", "Tulip", "Marigold"],
        "answer": "Lotus"
    },
    {
        "question": "National fruit?",
        "options": ["Mango", "Apple", "Banana", "Orange"],
        "answer": "Mango"
    }
]

current_q = 0
message = ""

# ---------- Main Loop ----------
running = True
while running:
    screen.fill(WHITE)
    q = quiz[current_q]

    # Draw question
    question_text = big_font.render(q["question"], True, BLACK)
    screen.blit(question_text, (50, 50))

    # Draw options as buttons
    buttons = []
    for i, option in enumerate(q["options"]):
        rect = pygame.Rect(100, 150 + i*70, 600, 50)
        pygame.draw.rect(screen, BLUE, rect)
        text_surf = font.render(option, True, WHITE)
        screen.blit(text_surf, (rect.x + 20, rect.y + 10))
        buttons.append((rect, option))

    # Display message
    msg_surf = font.render(message, True, BLACK)
    screen.blit(msg_surf, (50, 450))

    pygame.display.update()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for rect, option in buttons:
                if rect.collidepoint(mouse_pos):
                    if option.lower() == q["answer"].lower():
                        message = "Correct!"
                        lcd("Correct Answer")
                    else:
                        message = f"Wrong! Ans: {q['answer']}"
                        lcd("Wrong! " + q["answer"])
                    pygame.time.delay(1000)
                    current_q += 1
                    message = ""
                    if current_q >= len(quiz):
                        lcd("Quiz Over")
                        running = False
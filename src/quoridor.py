#!/bin/env python
# -*- coding: utf-8 -*-

import os
import pygame
from pygame.locals import *
from pygame import Color
import threading
import argparse
import time
from typing import Tuple

from .helpers import log, LogLevel
from . import config as cfg
from . import core

from .entities.board import Board


def dispatch(events, board: Board):
    for event in events:
        if event.type == QUIT:
            return False

        if hasattr(event, 'key'):
            if event.key == K_ESCAPE or board.finished:
                return False

        if board.computing or board.finished:
            continue

        if event.type == MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            board.onMouseClick(x, y)

        if event.type == MOUSEMOTION:
            x, y = pygame.mouse.get_pos()
            board.onMouseMotion(x, y)

    return True


# ----------------------- Welcome / UI helpers ----------------------- #
def draw_rounded_button(surface: pygame.Surface,
                        rect: pygame.Rect,
                        text: str,
                        font: pygame.font.Font,
                        base_color: Color,
                        hover_color: Color,
                        border_color: Color,
                        hovered: bool,
                        text_color: Color = Color(255, 255, 255),
                        radius: int = 10) -> None:
    """Draw a rounded button and centered text."""
    color = hover_color if hovered else base_color
    pygame.draw.rect(surface, color, rect, border_radius=radius)
    pygame.draw.rect(surface, border_color, rect, width=2, border_radius=radius)

    text_surf = font.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=rect.center)
    surface.blit(text_surf, text_rect)


def point_in_rect(point: Tuple[int, int], rect: pygame.Rect) -> bool:
    x, y = point
    return rect.left <= x <= rect.right and rect.top <= y <= rect.bottom


def fade_in_text(surface: pygame.Surface, text_surf: pygame.Surface, pos: Tuple[int, int], duration: float = 0.6):
    """Fade-in single text surface at pos over duration seconds."""
    clock = pygame.time.Clock()
    start = time.time()
    alpha = 0
    temp = text_surf.convert_alpha()
    while alpha < 255:
        t = time.time() - start
        alpha = min(255, int(255 * (t / duration)))
        temp.set_alpha(alpha)
        # redraw background caller must handle
        surface.blit(temp, pos)
        pygame.display.update()
        clock.tick(cfg.FRAMERATE)


def show_welcome_screen(screen: pygame.Surface) -> bool:
    """
    Display the splash / welcome screen.
    Returns True to continue to the game, False to exit.
    """
    # --- Layout & style ---
    screen_w, screen_h = screen.get_size()

    # Background colors (soft gradient simulation)
    top_color = Color(245, 238, 230)    # very light warm
    bottom_color = Color(225, 200, 170)  # light wood tone

    # Draw gradient-like background (simple vertical blend)
    for y in range(screen_h):
        # linear interpolation
        lerp = y / float(screen_h - 1)
        r = int(top_color.r * (1 - lerp) + bottom_color.r * lerp)
        g = int(top_color.g * (1 - lerp) + bottom_color.g * lerp)
        b = int(top_color.b * (1 - lerp) + bottom_color.b * lerp)
        pygame.draw.line(screen, (r, g, b), (0, y), (screen_w, y))

    # Title text
    title_font = pygame.font.Font(None, 72)
    subtitle_font = pygame.font.Font(None, 28)
    btn_font = pygame.font.Font(None, 28)

    title_text = title_font.render("Welcome to Quoridor", True, Color(40, 30, 20))
    subtitle_text = subtitle_font.render("Classic board — press Start to begin", True, Color(60, 50, 45))

    # Compute positions
    title_rect = title_text.get_rect(center=(screen_w // 2, screen_h // 3))
    subtitle_rect = subtitle_text.get_rect(center=(screen_w // 2, title_rect.bottom + 30))

    # Buttons
    btn_w, btn_h = 180, 48
    btn_gap = 24
    total_btn_width = btn_w * 2 + btn_gap
    left_x = (screen_w - total_btn_width) // 2

    start_rect = pygame.Rect(left_x, subtitle_rect.bottom + 50, btn_w, btn_h)
    exit_rect = pygame.Rect(left_x + btn_w + btn_gap, subtitle_rect.bottom + 50, btn_w, btn_h)

    start_base = Color(90, 160, 120)   # soft green
    start_hover = Color(115, 190, 145)
    exit_base = Color(180, 80, 70)     # muted red
    exit_hover = Color(205, 110, 100)
    border = Color(80, 60, 50)
    text_col = Color(255, 255, 255)

    # Fade-in effect for title and subtitle
    # We'll blit the previously drawn gradient background then fade-in title/subtitle
    screen.blit(title_text, title_rect)  # draw once to position
    screen.blit(subtitle_text, subtitle_rect)
    pygame.display.update()

    # Instead of pixel-by-pixel fade, do a short alpha ramp for title+subtitle
    title_surf = title_text.convert_alpha()
    subtitle_surf = subtitle_text.convert_alpha()
    clock = pygame.time.Clock()
    duration = 0.5
    start_time = time.time()
    while True:
        t = time.time() - start_time
        alpha = min(255, int(255 * (t / duration)))
        title_surf.set_alpha(alpha)
        subtitle_surf.set_alpha(alpha)
        # redraw gradient background
        for y in range(screen_h):
            lerp = y / float(screen_h - 1)
            r = int(top_color.r * (1 - lerp) + bottom_color.r * lerp)
            g = int(top_color.g * (1 - lerp) + bottom_color.g * lerp)
            b = int(top_color.b * (1 - lerp) + bottom_color.b * lerp)
            pygame.draw.line(screen, (r, g, b), (0, y), (screen_w, y))
        # blit faded texts
        screen.blit(title_surf, title_rect)
        screen.blit(subtitle_surf, subtitle_rect)
        pygame.display.update()
        clock.tick(cfg.FRAMERATE)
        if alpha >= 255:
            break

    # Welcome event loop
    running = True
    clicked_start = False
    hovered_start = False
    hovered_exit = False
    # small timer to prevent instant accidental double-press
    start_time = time.time()
    while running:
        clock.tick(cfg.FRAMERATE)

        # Redraw background + texts
        for y in range(screen_h):
            lerp = y / float(screen_h - 1)
            r = int(top_color.r * (1 - lerp) + bottom_color.r * lerp)
            g = int(top_color.g * (1 - lerp) + bottom_color.g * lerp)
            b = int(top_color.b * (1 - lerp) + bottom_color.b * lerp)
            pygame.draw.line(screen, (r, g, b), (0, y), (screen_w, y))

        screen.blit(title_text, title_rect)
        screen.blit(subtitle_text, subtitle_rect)

        mouse_pos = pygame.mouse.get_pos()
        hovered_start = point_in_rect(mouse_pos, start_rect)
        hovered_exit = point_in_rect(mouse_pos, exit_rect)

        # draw buttons
        draw_rounded_button(screen, start_rect, "Start", btn_font,
                            start_base, start_hover, border, hovered_start, text_col, radius=8)
        draw_rounded_button(screen, exit_rect, "Exit", btn_font,
                            exit_base, exit_hover, border, hovered_exit, text_col, radius=8)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                return False
            if event.type == KEYDOWN:
                # any key starts the game
                return True
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    if hovered_start:
                        clicked_start = True
                        return True
                    if hovered_exit:
                        return False
        # tiny delay to avoid 100% CPU
    # unreachable
    return False


# ----------------------- End welcome helpers ----------------------- #


def main() -> int:
    core.init()

    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--level",
                        help="AI player Level. Default is 0 (Easy). Higher is harder)",
                        default=cfg.LEVEL, type=int)

    parser.add_argument('-d', '--debug',
                        help="Debug mode", action='store_true')

    parser.add_argument('-C', '--cache',
                        help="Enable persistent memoize cache", action='store_true')

    options = parser.parse_args()
    cfg.LEVEL = options.level
    cfg.__DEBUG__ = options.debug
    cfg.CACHE_ENABLED = options.cache

    log('Quoridor AI game')
    log('Initializing system...')

    pygame.init()
    clock = pygame.time.Clock()
    pygame.display.set_mode((800, 600))
    pygame.display.set_caption(cfg.GAME_TITLE)
    screen = pygame.display.get_surface()

    # Show welcome screen BEFORE creating/drawing the board
    proceed = show_welcome_screen(screen)
    if not proceed:
        log('User exited from welcome screen. Bye!')
        pygame.quit()
        return 0

    # proceed with normal initialization
    screen.fill(Color(255, 255, 255))
    board = core.BOARD = Board(screen)
    board.draw()
    log('System initialized OK')

    if cfg.CACHE_ENABLED:
        if not os.path.exists(cfg.CACHE_DIR):
            log('Cache directory {} not found. Creating it...'.format(cfg.CACHE_DIR))
            os.makedirs(cfg.CACHE_DIR, exist_ok=True)

        if not os.path.isdir(cfg.CACHE_DIR):
            log('Could not create cache directory {}. Caching disabled'.format(cfg.CACHE_DIR), LogLevel.ERROR)
            cfg.CACHE_ENABLED = False

    cont = True
    while cont:
        clock.tick(cfg.FRAMERATE)
        pygame.display.flip()

        if not board.computing and not board.finished:
            if board.current_player.AI:
                board.computing = True
                thread = threading.Thread(target=board.computer_move)
                thread.start()

        cont = dispatch(pygame.event.get(), board)

    del board.rows

    pygame.quit()

    if cfg.CACHE_ENABLED:
        for pawn in board.pawns:
            if pawn.AI is not None:
                pawn.AI.flush_cache()

    log('Memoized nodes: %i' % core.MEMOIZED_NODES)
    log('Memoized nodes hits: %i' % core.MEMOIZED_NODES_HITS)

    for pawn in board.pawns:
        log('Memoized distances for [%i]: %i' % (pawn.id, pawn.distances.MEMO_COUNT))
        log('Memoized distances hits for [%i]: %i' % (pawn.id, pawn.distances.MEMO_HITS))

    log('Exiting. Bye!')
    return 0


if __name__ == '__main__':
    main()

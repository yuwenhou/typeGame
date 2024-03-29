import argparse

import pygame
from pygame.locals import *

from captions import Caption
from inputarea import InputArea


class GUI():
    '''
    图形用户界面
    '''
    def __init__(self, textSource):
        self.speedLimit = 70
        self.clock = pygame.time.Clock()
        self.screenRect = Rect(0, 0, 640, 480)
        self.screen = pygame.display.set_mode(self.screenRect.size)
        self.background = pygame.Surface(self.screenRect.size).convert()
        self.elements = pygame.sprite.RenderUpdates()
        self.inputArea = InputArea(textSource)
        self.caption = Caption()

        self.elements.add(self.caption)
        self.background.fill((255, 255, 255))
        self.screen.blit(self.background, (0, 0))
        pygame.display.set_caption('SUPER TYPIST')
        pygame.display.update()

    def start(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return
                    # 忽视功能键
                    if len(event.unicode) > 0:
                        self.inputArea.keyin(event.unicode)

            typingSpeed = self.inputArea.getSpeed()
            words = self.inputArea.getWords()
            corrWords = self.inputArea.getCorrWords()
            self.caption.setText(typingSpeed, words, corrWords)

            # 根据打字速度改变背景颜色
            if typingSpeed > self.speedLimit:
                typingSpeed = self.speedLimit
            self.screen.fill([(int)(255-255*typingSpeed/self.speedLimit),
                              (int)(255*typingSpeed/self.speedLimit),
                              0])

            self.inputArea.update()
            self.elements.update()
            self.elements.draw(self.screen)
            pygame.display.update()
            self.clock.tick(30)


def main():
    parser = argparse.ArgumentParser(description="Typing exercice.")
    parser.add_argument('--f',
                        help="path for the text you would like to type",
                        default='files/speed.txt')
    args = parser.parse_args()

    pygame.init()
    ui = GUI(args.f)
    ui.start()


if __name__ == '__main__':
    main()
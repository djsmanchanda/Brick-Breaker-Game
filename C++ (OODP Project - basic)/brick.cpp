#include <iostream>
#include <SDL2/SDL.h>
#include <SDL2/SDL_ttf.h>

const int SCREEN_WIDTH = 800;
const int SCREEN_HEIGHT = 600;
const int PADDLE_WIDTH = 100;
const int PADDLE_HEIGHT = 20;
const int BALL_SIZE = 20;
const int BRICK_WIDTH = 80;
const int BRICK_HEIGHT = 30;
const int NUM_BRICKS = 40;

class Paddle {
public:
    int x, y, width, height, speed;

    Paddle() : x(SCREEN_WIDTH / 2 - PADDLE_WIDTH / 2), y(SCREEN_HEIGHT - 2 * PADDLE_HEIGHT),
               width(PADDLE_WIDTH), height(PADDLE_HEIGHT), speed(10) {}

    void moveLeft() {
        x -= speed;
        if (x < 0) {
            x = 0;
        }
    }

    void moveRight() {
        x += speed;
        if (x + width > SCREEN_WIDTH) {
            x = SCREEN_WIDTH - width;
        }
    }
};

class Ball {
public:
    int x, y, size, speedX, speedY;

    Ball() : x(SCREEN_WIDTH / 2 - BALL_SIZE / 2), y(SCREEN_HEIGHT / 2 - BALL_SIZE / 2),
             size(BALL_SIZE), speedX(3), speedY(-3) {}

    void move() {
        x += speedX;
        y += speedY;

        if (x < 0 || x + size > SCREEN_WIDTH) {
            speedX = -speedX;
        }

        if (y < 0) {
            speedY = -speedY;
        }
    }
};

class Brick {
public:
    int x, y, width, height, health;

    // Default constructor
    Brick() : x(0), y(0), width(BRICK_WIDTH), height(BRICK_HEIGHT), health(1) {}

    // Constructor with arguments
    Brick(int posX, int posY) : x(posX), y(posY), width(BRICK_WIDTH), height(BRICK_HEIGHT), health(1) {}
};

class Game {
public:
    Paddle paddle;
    Ball ball;
    Brick bricks[NUM_BRICKS];
    int points;
    bool gameEnded;

    Game() : points(0), gameEnded(false) {
        // Initialize bricks
        int brickIndex = 0;
        for (int i = 0; i < 4; ++i) {
            for (int j = 0; j < 10; ++j) {
                bricks[brickIndex++] = Brick(j * BRICK_WIDTH, i * BRICK_HEIGHT);
            }
        }
    }

    void handleInput(SDL_Event& event) {
        if (event.type == SDL_QUIT) {
            exit(0);
        }
        else if (event.type == SDL_KEYDOWN) {
            switch (event.key.keysym.sym) {
                case SDLK_LEFT:
                    paddle.moveLeft();
                    break;
                case SDLK_RIGHT:
                    paddle.moveRight();
                    break;
                default:
                    break;
            }
        }
    }

    void update() {
        if (!gameEnded) {
            ball.move();

            // Check for collisions with paddle
            if (ball.y + ball.size > paddle.y && ball.x + ball.size > paddle.x &&
                ball.x < paddle.x + paddle.width) {
                ball.speedY = -ball.speedY;
            }

            // Check for collisions with bricks
            for (int i = 0; i < NUM_BRICKS; ++i) {
                if (bricks[i].health > 0 &&
                    ball.x + ball.size > bricks[i].x && ball.x < bricks[i].x + bricks[i].width &&
                    ball.y + ball.size > bricks[i].y && ball.y < bricks[i].y + bricks[i].height) {
                    ball.speedY = -ball.speedY;
                    bricks[i].health--;
                    points += 10; // Increment points when a brick is destroyed

                    // Check if all bricks are destroyed
                    if (allBricksDestroyed()) {
                        gameEnded = true;
                    }
                }
            }

            // Check if the ball is below the paddle
            if (ball.y + ball.size > paddle.y + paddle.height) {
                gameEnded = true;
            }
        }
    }

    void render(SDL_Renderer *renderer) {
        // Clear the screen
        SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255);
        SDL_RenderClear(renderer);

        if (!gameEnded) {
            // Draw the paddle
            SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255);
            SDL_Rect paddleRect = {paddle.x, paddle.y, paddle.width, paddle.height};
            SDL_RenderFillRect(renderer, &paddleRect);

            // Draw the ball
            SDL_Rect ballRect = {ball.x, ball.y, ball.size, ball.size};
            SDL_RenderFillRect(renderer, &ballRect);

            // Draw the bricks
            for (int i = 0; i < NUM_BRICKS; ++i) {
                if (bricks[i].health > 0) {
                    SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255);
                    SDL_Rect brickRect = {bricks[i].x, bricks[i].y, bricks[i].width, bricks[i].height};
                    SDL_RenderFillRect(renderer, &brickRect);
                }
            }

            // Display points
            SDL_Color textColor = {255, 255, 255, 255};
            std::string pointsText = "Points: " + std::to_string(points);
            renderText(renderer, pointsText, 10, 10, textColor);
        }
        else {
            // Display game-ended message
            SDL_Color textColor = {255, 255, 255, 255};
            std::string endMessage = "Game Over! Points: " + std::to_string(points);
            renderText(renderer, endMessage, SCREEN_WIDTH / 4, SCREEN_HEIGHT / 2, textColor);
            std::string authors = "Made by Divjot and Charishma";
            renderText(renderer, authors, SCREEN_WIDTH / 4, SCREEN_HEIGHT / 2 + 40, textColor);
        }

        // Present the renderer
        SDL_RenderPresent(renderer);
    }

    bool allBricksDestroyed() const {
        for (int i = 0; i < NUM_BRICKS; ++i) {
            if (bricks[i].health > 0) {
                return false;
            }
        }
        return true;
    }

    void renderText(SDL_Renderer *renderer, const std::string& text, int x, int y, const SDL_Color& color) {
        // This function renders text using SDL_ttf library
        // Make sure to have SDL_ttf installed on your system

        TTF_Font* font = TTF_OpenFont("C:/Windows/Fonts/Arial.ttf", 24); 

        if (font == nullptr) {
            std::cerr << "TTF_OpenFont error: " << TTF_GetError() << std::endl;
            return;
        }

        SDL_Surface* surface = TTF_RenderText_Solid(font, text.c_str(), color);

        if (surface == nullptr) {
            std::cerr << "TTF_RenderText_Solid error: " << TTF_GetError() << std::endl;
            TTF_CloseFont(font);
            return;
        }

        SDL_Texture* texture = SDL_CreateTextureFromSurface(renderer, surface);

        if (texture == nullptr) {
            std::cerr << "SDL_CreateTextureFromSurface error: " << SDL_GetError() << std::endl;
            SDL_FreeSurface(surface);
            TTF_CloseFont(font);
            return;
        }

        SDL_Rect textRect = {x, y, surface->w, surface->h};
        SDL_RenderCopy(renderer, texture, nullptr, &textRect);

        SDL_FreeSurface(surface);
        SDL_DestroyTexture(texture);
        TTF_CloseFont(font);
    }
};

int SDL_main(int argc, char* argv[]) {
    
    // Initialize SDL
    if (SDL_Init(SDL_INIT_VIDEO) != 0) {
        std::cerr << "SDL_Init error: " << SDL_GetError() << std::endl;
        return 1;
    }

    // Initialize SDL_ttf for rendering text
    if (TTF_Init() != 0) {
        std::cerr << "TTF_Init error: " << TTF_GetError() << std::endl;
        SDL_Quit();
        return 1;
    }

    // Create window
    SDL_Window *window = SDL_CreateWindow("Brick Breaker", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED,
                                          SCREEN_WIDTH, SCREEN_HEIGHT, SDL_WINDOW_SHOWN);
    if (window == nullptr) {
        std::cerr << "SDL_CreateWindow error: " << SDL_GetError() << std::endl;
        TTF_Quit();
        SDL_Quit();
        return 1;
    }

    // Create renderer
    SDL_Renderer *renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);
    if (renderer == nullptr) {
        std::cerr << "SDL_CreateRenderer error: " << SDL_GetError() << std::endl;
        SDL_DestroyWindow(window);
        TTF_Quit();
        SDL_Quit();
        return 1;
    }

    // Set up the game
    Game game;
    SDL_Delay(2000);

    // Game loop
    bool quit = false;
    SDL_Event event;
    while (!quit) {
        // Handle input
        while (SDL_PollEvent(&event)) {
            game.handleInput(event);
            if (event.type == SDL_QUIT) {
                quit = true;
            }
        }

        // Update game state
        game.update();

        // Render the game
        game.render(renderer);

        // Add a short delay to control the frame rate
        SDL_Delay(10);
    }

    // Clean up and exit
    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    TTF_Quit();
    SDL_Quit();

    return 0;
}

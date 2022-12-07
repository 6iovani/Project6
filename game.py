# ----NAME-----
# Giovani Martins

# ----HOW TO PLAY-------
# use mouse to move and space bar to shoot

# ----EXTRAS------
# I was searching through the web and learned how to make a moving background with arcade

# -----PROBLEMS I COULDN'T FIX-----
# program still runs even if player wins or lose so the score or lives may change
# winning and losing sound keeps replaying many times over really fast as if it was in a for loop so I used
# time.sleep to slow it down
# couldn't find a good sound for when player loses a life so I used the same sound from when player loses the game
# might be a problem just on my end but if shooting doesn't work save the program then run it again and it should work

import random
import arcade
import time

class Fireball(arcade.Sprite):
    def update(self):
        speed = 4
        self.center_y += speed

class Enemy(arcade.Sprite):
    def update(self):

        drop_speed = random.randrange(-3, 2)
        movement = random.randrange(-2, 3)

        # do the moves
        self.center_y += drop_speed
        self.center_x += movement


class MyGame(arcade.Window):

    def __init__(self):

        # Call the parent class initializer
        super().__init__(1200, 720, "Shooter Game")

        # sprite lists variables
        self.player_list = None
        self.enemies_list = None
        self.fireball_list = None

        # player info
        self.player_sprite = None
        self.score = 0
        self.life = 3
        self.player_sprite_dx = 0
        self.player_sprite_dy = 0

        # sounds
        self.shoot_sound = None
        self.kill_sound = None
        self.winning_sound = None
        self.losing_sound = None
        self.enemy_sound = None

        # startpoint of the moving background
        self.line_start = -1

    def setup(self):

        # setting up sprites in sprite lists variables
        self.player_list = arcade.SpriteList()
        self.enemies_list = arcade.SpriteList()
        self.fireball_list = arcade.SpriteList()

        # sound effects
        self.shoot_sound = arcade.sound.load_sound("mixkit-arrow-whoosh-1491.wav")
        self.wining_sound = arcade.load_sound("mixkit-achievement-bell-600.wav")
        self.losing_sound = arcade.load_sound("mixkit-arcade-retro-game-over-213.wav")
        self.enemy_sound = arcade.load_sound("mixkit-falling-hit-on-gravel-756.wav")

        # giving player placement and a sprite
        self.player_sprite = arcade.Sprite("sceptre-of-fire.png", 1)
        self.player_sprite.center_x = 400
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

        # giving enemies placement and movement
        for i in range(50):

            enemy = Enemy("assassin-idle-4.png")
            enemy.center_x = random.randrange(1200)
            enemy.center_y = random.randrange(500, 1200)
            self.enemies_list.append(enemy)

        # background color
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):

        arcade.start_render()
        if self.score >= 20:
            arcade.play_sound(self.wining_sound)
            arcade.draw_text(f"You Won! SCORE: {self.score} LIVES: {self.life}", 330, 500, arcade.color.WHITE, 30)
            arcade.draw_text(f"You can now exit the program, or listen keep listening to this sound forever ", 305, 400, arcade.color.WHITE, 15)
            arcade.finish_render()
            time.sleep(3)
            return

        if self.life <= 0:
            arcade.play_sound(self.losing_sound)
            arcade.draw_text(f"Game Over! SCORE: {self.score} LIVES: {self.life}", 330, 500, arcade.color.WHITE, 30)
            arcade.draw_text(f"You can now exit the program, or listen keep listening to this sound forever ", 305, 400, arcade.color.WHITE, 15)
            arcade.finish_render()
            time.sleep(3)
            return


        # draw the score and lives text
        arcade.draw_text(f"Score: {self.score}", 3, 5, arcade.color.DARK_RED, 15)
        arcade.draw_text(f"Lives: {self.life}", 100, 5, arcade.color.WHITE, 15)

          # move the background
        if self.line_start < 49:
            self.line_start += 1
        else:
            self.line_start = 0

        # draw horizontal/vertical lines every 50 pixels
        for x in range(0, 1200, 50):
            arcade.draw_line(x + self.line_start, 0, x + self.line_start, 720, arcade.color.GO_GREEN, 2)

        for y in range(0, 720, 50):
            arcade.draw_line(0, y + self.line_start, 1200, y + self.line_start, arcade.color.GO_GREEN, 2)

        # draw all the sprites.
        self.enemies_list.draw()
        self.fireball_list.draw()
        self.player_sprite.draw()

        arcade.finish_render()

    def on_key_press(self, symbol, modifiers):

        # create and position the fireball
        if symbol == arcade.key.SPACE:

            fireball = Fireball("shot2.gif", 1)
            arcade.play_sound(self.shoot_sound)
            fireball.center_x = self.player_sprite.center_x
            fireball.bottom = self.player_sprite.top
            self.fireball_list.append(fireball)





    def on_mouse_motion(self, x, y, dx, dy):

        # give player movement control with mouse motion
        self.player_sprite.center_x = x

    def update(self, delta_time):

        self.enemies_list.update()
        self.fireball_list.update()

        # check to see player killed an enemy and remove them
        for fireball in self.fireball_list:

            kill = arcade.check_for_collision_with_list(fireball, self.enemies_list)
            if len(kill) > 0:
                arcade.play_sound(self.enemy_sound)
                fireball.remove_from_sprite_lists()

            for enemy in kill:
                enemy.remove_from_sprite_lists()
                self.score += 1


        for enemy in self.enemies_list:

            lives = arcade.check_for_collision_with_list(enemy, self.player_list)
            if len(lives) > 0:
                arcade.play_sound(self.losing_sound)
                enemy.remove_from_sprite_lists()
                self.life -= 1















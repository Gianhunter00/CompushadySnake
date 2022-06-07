from compushady import Buffer, Swapchain, Texture2D
from compushady.shaders import hlsl
import compushady.config
import compushady.formats
import glfw
from timer import game_timer
from snake import Snake,PowerUp
from shader import shader_clean_screen, shader_code

class Game():
    def init(self):
        glfw.init()
        glfw.window_hint(glfw.CLIENT_API, glfw.NO_API)
        self.window = glfw.create_window(512,512,'Hello World', None, None)
        self.swapchain = Swapchain(glfw.get_win32_window(self.window), compushady.formats.B8G8R8A8_UNORM, 3)

        self.quads_staging_buffer = Buffer(8 * 8 * 8, compushady.HEAP_UPLOAD)
        self.quads_buffer = Buffer(self.quads_staging_buffer.size, format=compushady.formats.R32G32B32A32_SINT)

        self.target = Texture2D(512, 512, compushady.formats.B8G8R8A8_UNORM)
        world_size = [self.target.width, self.target.height]
        self.power_up = PowerUp(world_size)
        self.player = Snake(world_size, self.power_up)

        self.compute_clean_screen = compushady.Compute(hlsl.compile(shader_clean_screen), uav=[self.target])
        self.compute_shader_code = compushady.Compute(hlsl.compile(shader_code), srv=[self.quads_buffer], uav=[self.target])

        self.timer = game_timer(0.1)
        
    def update(self):
        while not glfw.window_should_close(self.window):
            glfw.poll_events()
            self.player.input(self.window)
            if(self.timer.tick()):
                self.player.move()
                if not self.player.alive:
                    break
                self.compute_clean_screen.dispatch(self.target.width, self.target.height, 1)
                self.quads_staging_buffer.upload(self.player.pack_snake() + self.power_up.pack())
                self.quads_staging_buffer.copy_to(self.quads_buffer)
                self.compute_shader_code.dispatch(self.target.width // 8, self.target.height // 8, self.player.line + 2)
            self.swapchain.present(self.target)

    def destroy(self):
        self.swapchain = None
        glfw.terminate()
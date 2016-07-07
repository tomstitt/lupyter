from ipykernel.kernelbase import Kernel
import lup

class LuaKernel(Kernel):
    implementation = "iPython"
    implementation_version = "1"
    language_info = {
        'name': 'Lua',
        'file_extension': '.lua',
        'version': '5.X.Y',
        'mimetype': 'text/Lua'
    }
    banner = "Lua Kernel - Layered like an Onion"
    luastate = None

    def do_execute(self, code, silent, store_history=True,
                   user_expression=None, allow_stdin=False):
        if not self.luastate:
            self.luastate = lup.LuaState()
        if not silent:
            stream_content = {
                'name': 'stdout',
                'text': lup.process_chunk(self.luastate, code)
            }
            self.send_response(self.iopub_socket, 'stream', stream_content)

        return {
            'status': 'ok',
            'execution_count': self.execution_count,
            'payload': [],
            'user_expression': {}
        }


if __name__ == "__main__":
    from ipykernel.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=LuaKernel)

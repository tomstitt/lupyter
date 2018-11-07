from ipykernel.kernelbase import Kernel

from lup import LuaState


class LuaKernel(Kernel):
    implementation = "iPython"
    implementation_version = "1"
    banner = "Lua"
    language_info = {
        "name": "Lua",
        "file_extension": ".lua",
        "version": "5",
        "mimetype": "text/Lua"
    }

    def stdout(self, text):
        self.send_response(self.iopub_socket, "stream", {
            "name": "stdout",
            "text": text})

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.luastate = LuaState(lambda text: self.stdout(text))

    def do_execute(self, code, silent, store_history=True, user_expression=None, allow_stdin=False):
        self.luastate.eval(code)

        return {
            'status': 'ok',
            'execution_count': self.execution_count,
            'payload': [],
            'user_expression': {}
        }


if __name__ == "__main__":
    from ipykernel.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=LuaKernel)
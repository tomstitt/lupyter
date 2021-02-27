from ipykernel.kernelbase import Kernel
from .lua_runtime import LuaRuntime

try:
    from .versions import lua_version
except ImportError:
    lua_version = "5.1.0"

class LuaKernel(Kernel):
    implementation = "iPython"
    implementation_version = "1"
    banner = "Lua"
    language_info = {
        "name": "lua",
        "file_extension": ".lua",
        "version": lua_version,
        "mimetype": "text/x-lua"
    }

    def stdout(self, text):
        self.send_response(self.iopub_socket, "stream", {
            "name": "stdout",
            "text": text})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lua = LuaRuntime(lambda text: self.stdout(text))

    def do_execute(self, code, silent, store_history=True, user_expression=None, allow_stdin=False):
        # TODO: doc lookup
        if code.startswith("?") or code.endswith("?"):
            pass
        else:
            self.lua.eval(code)

        return {
            "status": "ok",
            "execution_count": self.execution_count,
            "payload": [],
            "user_expression": {}
        }

    def do_complete(self, code, cursor_pos):
        matches, cursor_start = self.lua.complete(code, cursor_pos)
        return {
            "status": "ok",
            "matches": matches,
            "cursor_start": cursor_start,
            "cursor_end": cursor_pos,
            "metadata": None
        }


if __name__ == "__main__":
    from ipykernel.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=LuaKernel)

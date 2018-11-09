from ipykernel.kernelbase import Kernel

from .c_interface import LuaState


class LuaKernel(Kernel):
    implementation = "iPython"
    implementation_version = "1"
    banner = "Lua"
    language_info = {
        "name": "lua",
        "file_extension": ".lua",
        "version": "5",
        "mimetype": "text/x-lua"
    }

    def stdout(self, text):
        self.send_response(self.iopub_socket, "stream", {
            "name": "stdout",
            "text": text})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.luastate = LuaState(lambda text: self.stdout(text))

    def do_execute(self, code, silent, store_history=True, user_expression=None, allow_stdin=False):
        # TODO: doc lookup
        if code.startswith("?") or code.endswith("?"):
            pass
        else:
            self.luastate.eval(code)

        return {
            "status": "ok",
            "execution_count": self.execution_count,
            "payload": [],
            "user_expression": {}
        }

    def do_complete(self, code, cursor_pos):
        matches, cursor_start = self.luastate.complete(code, cursor_pos)
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

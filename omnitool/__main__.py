import sys

import multiprocessing

from . import themename, get_plugins, plugins, run
from .relay import launch_plugin

child = False

multiprocessing.freeze_support()
multiprocessing.set_start_method("spawn")  # Prevents X11 crash on Linux - properly separates pygame internals
for arg in sys.argv:
    if "multiprocessing" in arg:
        child = True
        break

if not child:
    try:
        from .splashlib import splash
        splash((512, 512), "Omnitool", os.path.join("themes", themename, "Splash.png"))
    except Exception as e:
        print("SplashWarning: " + str(e))


try:
    from .render import run as _
except:
    if not child:
        print("WorldRender extension not available:")
        import traceback

        traceback.print_exc()
    render_ext = False
else:
    render_ext = True


if not child:
    get_plugins()
    p = False
    for arg in sys.argv:
        if arg.startswith("plugin:"):
            p = True
            name = arg[7:]
            for ps in plugins:
                if ps[0] == name:
                    print("Launching plugin %s" % ps[1])
                    pygame.quit()
                    start_proc((launch_plugin, [ps[1], ps]))
                    sys.exit()
            print("Plugin not found")

    if not p:
        run()
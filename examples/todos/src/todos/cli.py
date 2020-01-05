import argparse

from dotenv import find_dotenv, load_dotenv
from werkzeug.serving import run_simple


def get_options():
    parser = argparse.ArgumentParser(prog='Todos example for Kristall web framework')
    parser.add_argument(
        '--host', default='127.0.0.1', help='Host name or IP address to bind to'
    )
    parser.add_argument('--port', type=int, default=5000, help='Port number')
    parser.add_argument(
        '--no-reload', action='store_true', default=False,
        help='Flag to turn off code autoreload',
    )
    parser.add_argument(
        '--debug', action='store_true', default=False,
        help='Flag to turn off built-in debugger',
    )
    return parser.parse_args()


def main():
    opts = get_options()
    load_dotenv(find_dotenv())
    use_reloader = not opts.no_reload
    use_debugger = opts.debug
    from .app import create_app
    app = create_app()
    run_simple(
        opts.host, opts.port, app, use_reloader=use_reloader, use_debugger=use_debugger
    )


if __name__ == '__main__':
    main()

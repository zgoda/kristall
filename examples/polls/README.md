# Polls example for Kristall

This is larger application example for Kristall that shows its intended usage.

## Backend

Create virtualenv with Python>=3.7 and install backend code:

```shell
/usr/bin/python3.7 -m venv venv
source venv/bin/activate
pip install -U pip wheel
pip install -U -e .[dev]
```

You can launch it as `polls run``.

Application uses [TinyDB](https://pypi.org/project/tinydb/) to store data, with sample data provided.

## Frontend

Frontend application is written in Javascript using [Preact UI framework](https://preactjs.com/), with [Picnic](https://picnicss.com/) as CSS library. Change to `ui` directory and initialize application:

```shell
cd ui
npm install
```

Frontend application is configured to proxy requests from Javascript code to backend running on port 5000. Run it with `npm`:

```shell
npm run dev
```

If you change port or host of your backend you will need to update frontend proxy configuration in `ui/preact.config.js`.

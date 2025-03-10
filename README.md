# ProxyFinder

ProxyFinder is a Python tool for downloading and testing proxies that work on your system. It supports normal and JSON output formats and can generate a configuration file for the ProxyChains tool.

## Features
- Fetch up to 1000 proxies.
- Check which proxies are working.
- Output results in JSON format.
- Generate a ProxyChains configuration file.

## Installation
```sh
pip install -r requirements.txt
```

## Usage
Run ProxyFinder with the following options:
```sh
python proxyfinder.py --working      # Get only working proxies
python proxyfinder.py --proxychains  # Generate a ProxyChains configuration file
```

You can combine options as needed:
```sh
python proxyfinder.py --working --json
```

## Output Examples
### Normal Output
```json
[
  {
    "ip": "27.79.194.186",
    "protocols": [
      "http"
    ],
    "port": "16000",
    "responseTime": 404
  },
  {
    "ip": "123.30.154.171",
    "protocols": [
      "http"
    ],
    "port": "7777",
    "responseTime": 144
  },
]  
```

### ProxyChain Output
```json
http 27.79.194.186 16000
http 123.30.154.171 7777
```

## License
MIT License


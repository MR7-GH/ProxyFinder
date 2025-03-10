# ProxyFinder

ProxyFinder is a Python tool for downloading and testing proxies that work on your system. It supports normal and JSON output formats and can generate a configuration file for the ProxyChains tool.

## Features
- Fetch up to 1000 proxies.
- Check which proxies are working.
- Output results in normal or JSON format.
- Generate a ProxyChains configuration file.

## Installation
```sh
pip install -r requirements.txt
```

## Usage
Run ProxyFinder with the following options:
```sh
python proxyfinder.py --all          # Get all 1000 proxies (without testing)
python proxyfinder.py --working      # Get only working proxies
python proxyfinder.py --json         # Output in JSON format
python proxyfinder.py --proxychains  # Generate a ProxyChains configuration file
```

You can combine options as needed:
```sh
python proxyfinder.py --working --json
```

## Output Examples
### Normal Output
```
Fetching proxies...
Testing proxies...
Working proxies:
123.45.67.89:8080
98.76.54.32:3128
```

### JSON Output
```json
{
  "working_proxies": [
    "123.45.67.89:8080",
    "98.76.54.32:3128"
  ]
}
```

## License
MIT License


import argparse

parser = argparse.ArgumentParser()
parser.add_argument("format", help="Format to conversion", type=str)
parser.add_argument("sql", help="Multitran SQL file", type=str)
parser.add_argument("-o", "--output", help="Output file", type=str)
parser.add_argument("--sort", help="Sort keys", action="store_true")
parser.add_argument("--indent", help="JSON Indent", type=int, default=None)
parser.add_argument("--ensure-ascii", help="JSON Ensure ASCII", action="store_true")
args = parser.parse_args()

if args.format == "json":
    import multitran2json
    import json

    sort_keys = False
    ensure_ascii = False
    out = "file.json"
    if args.sort:
        sort_keys = True
    if args.ensure_ascii:
        ensure_ascii = True
    if args.output:
        out = args.output

    # print(json.dumps(multitran2json.convert(args.sql),
    #                  ensure_ascii=ensure_ascii, indent=args.indent, sort_keys=sort_keys))

    with open(out, "w") as write_file:
        json.dump(multitran2json.convert(args.sql),
                  ensure_ascii=ensure_ascii, indent=args.indent, sort_keys=sort_keys, fp=write_file)

    print("Saved as", out)
else:
    print("Unknown format", args.format)
    parser.print_help()

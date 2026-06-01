import argparse
import csv
from pathlib import Path
from print_layer import PrintLayer
from print_mode import PrintMode
from print_layer_summary import PrintSummary

def main():
    parser = argparse.ArgumentParser(
        description="Process print jobs with specified configuration.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Examples:\n"
               "  python main.py --print-name 'test print' --output-folder ./output --mode 'supervised'\n"
               "  python main.py -n 'test print 2' -o ./output -m 'automatic'\n"
    )

    parser.add_argument(
        "--print-name", "-n",
        type=str,
        required=True,
        help="Name identifier for the print job/output"
    )
    parser.add_argument(
        "--output-folder", "-o",
        type=str,
        required=True,
        help="Destination directory for output files"
    )
    parser.add_argument(
        "--mode", "-m",
        type=str,
        default="automatic",
        choices=["supervised", "automatic"],
        help="Execution mode: 'supervised' or 'automatic' (default: automatic)"
    )

    args = parser.parse_args()

    if args.mode == "supervised":
        print("mode: supervised")
        print_mode = PrintMode.SUPERVISED
    else:
        print("mode: automatic")
        print_mode = PrintMode.AUTOMATIC

    # path to the print gcode (or in this case, the csv file)
    print_layers_data_path = Path("fl_coding_challenge_v1.csv")

    # path to the output file
    print_layers_output_path = Path(args.output_folder) / (args.print_name + ".jsonl")

    # start processing the gcode
    print_summary = process_print_layers(print_layers_data_path, print_layers_output_path, print_mode)

    # print summary
    print(f"total print height: {print_summary.print_height:.3f}")
    
    print(f"errors during print:")
    for print_error in print_summary.get_errors():
        print(f"\t{print_error}")

def process_print_layers(print_layers_data_path: Path, print_layers_output_path: Path, print_mode: PrintMode):
    print_summary = PrintSummary()

    with open(print_layers_data_path, "r", encoding="utf-8") as f:
        file_line_count = sum(1 for _ in f)

    line_idx = 0
    with open(print_layers_data_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader) # skip the header row of the csv file
        
        with open(print_layers_output_path, "w") as out_file:
            for row in reader:
        
                line_idx += 1
                print(f"line [{line_idx}/{file_line_count}]")

                if print_mode == PrintMode.SUPERVISED:
                    print("Press \"Enter\" to print the next layer:")
                    input()
                print_layer = PrintLayer.from_csv_row(row)
                
                layer_summary = process_print_layer(print_layer, out_file, print_mode)

                if layer_summary is None:
                    continue

                if layer_summary["exit"] is True:
                    return print_summary

                if layer_summary["layer_height"] is not None:
                    print_summary.print_height += layer_summary["layer_height"]

                if "error" in layer_summary and layer_summary["error"]:
                    print_summary.add_error(layer_summary["error"])
    
    return print_summary

def process_print_layer(print_layer: PrintLayer, out_file, print_mode: PrintMode):
    layer_summary = {}
    layer_summary["exit"] = False

    # check for errors
    error_occurred = False

    if print_layer.layer_error != "SUCCESS":
        layer_summary["error"] = print_layer.layer_error
        error_occurred = True

    # I am considering the lack of a layer image an error for this test. 
    # I figure the whole point of supervised mode is to alert the user if anything goes awry, which I think a missing image qualifies for.
    if print_layer.image_data == "":
        layer_summary["error"] = "IMAGE_NOT_FOUND"
        error_occurred = True
    
    if error_occurred == True and print_mode == PrintMode.SUPERVISED:
        # alert user that an error has occurred during the print
        print(f"ERROR: {layer_summary["error"]}")
        print(f"Continue? [Y/n]")
        user_input = input()
        if user_input == "n":
            layer_summary["exit"] = True
            return layer_summary

    # "print" the layer
    out_file.write(print_layer.to_jsonl())
    out_file.write(str("\n"))

    layer_summary["layer_height"] = print_layer.layer_height

    return layer_summary

if __name__ == "__main__":
    main()
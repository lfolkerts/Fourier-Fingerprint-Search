import helper as _hp
import database as _db
import fingerprint as _fp
import score as _sc
import search as _search
import sys
from tqdm import tqdm

def main():
    # parse arguments
    stl_files, mode, destroyDB = _hp.parseArgs()

    # Delete database if the flag is set
    if destroyDB:
        _db.destroy_db('./avocado_db')
        if mode == 'search':
            sys.exit(0)

    # Open (or create) database
    db = _db.Database('./avocado_db')

    if _hp.VERBOSE:
        print('Generating fingerprint of', stl_files, 'with:',
        '\n\tNumber of matches to return :', str(_hp.NUMBER_OF_MATCHES),
        '\n\tFan value :', str(_hp.FAN_VALUE),
        '\n\tNumber of slices :', str(_hp.NUM_OF_SLICES),
        '\n\tNumber of peaks :', str(_hp.NUM_OF_PEAKS),
        '\n\tGrid size :', str(_hp.GRID_SIZE),
        '\n\tRotate flag :', str(_hp.ROTATE),
        '\n\tStar rotate :', str(_hp.STAR_ROTATE),
        '\n\tInterpolation flag :', str(_hp.INTERP),
        '\n\tMin number of signatures to match within a neighborhood :', str(_hp.MIN_SIGNATURES_TO_MATCH),
        '\n')

    # Disable progress bar if only one
    disable_tqdm = False
    if len(stl_files) < 2:
        disable_tqdm = True

    if mode == 'learn':
        print('Enrolling fingerprint(s) to the database...')

    # For each file
    for stl_file in tqdm(stl_files, ncols=100, bar_format='[{n_fmt}/{total_fmt}] {l_bar}{bar}|', disable=disable_tqdm):
        # generate fingerprint of the file
        neighborhoods = _fp.fingerprint(stl_file, _hp.NUM_OF_SLICES, _hp.NUM_OF_PEAKS, _hp.FAN_VALUE, _hp.ROTATE, _hp.INTERP, _hp.STAR_ROTATE)

        # Add fingerprint to database
        if mode == 'learn':
            db.add_signatures(neighborhoods, stl_file)
        # Search in database for potential matches
        else: # mode == 'search':
            anchor_matches, signatures_matches = _db.weighted_search_signatures(db, neighborhoods)

            matches = None
            if _hp.PRINT_NAIVE:
                print('\nFiles matched with ' + stl_file + ' using the number of signatures : ', end='')
                matches = signatures_matches
                _hp.print_lst_of_tuples(matches)
                print("Signature Match Score: ", _sc.score(matches, stl_file, 100), "\n")

            if _hp.NEIGHBORHOODS:
                print('\nFiles matched with ' + stl_file + ' using the number of neighborhoods : ', end='')
                matches = anchor_matches
                _hp.print_lst_of_tuples(matches)
                print("Neighborhood Match Score: ", _sc.score(matches, stl_file, 100), "\n")

            if _hp.EXPORT_PNGS or _hp.SHOW_PNGS:
                _hp.export_pngs([i[0] for i in matches], _hp.SHOW_PNGS)

    # Close the database
    db.close_db()

if __name__ == "__main__":
    main()

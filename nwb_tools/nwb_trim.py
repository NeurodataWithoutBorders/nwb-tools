import argparse
import h5py
import warnings

# NOTE: h5repack is not guaranteed to be installed, so avoid using it

# maximum length of each dimension of a dataset to copy
MAX_SHAPE_PER_DIM = 10  # TODO make this user specifiable


def main():
    parser = argparse.ArgumentParser('python nwb_trim.py')
    parser.add_argument('-o', '--output', dest='output',
                        help=('output filename (if not supplied, then "_trim" is appended to the name of the input '
                              'file)'))
    parser.add_argument('path', help='path to an NWB file')
    args = parser.parse_args()

    if not args.path.endswith('.nwb'):
        raise ValueError('Path must point to an NWB file.')
    nwb_trim(args.path, args.output)


def nwb_trim(in_path, out_path):
    with h5py.File(in_path, 'r') as f_in:
        with h5py.File(out_path, 'w') as f_out:
            copy_group(f_in['/'], f_out)


def copy_group(group, f_out):
    # NOTE we cannot access the track_order property so we cannot copy it
    new_group = f_out.create_group(name=group.path)
    copy_attributes(group, new_group)

    for key, sub_obj in group.items():
        link_type = group.get(key, getlink=True)
        if isinstance(link_type, (h5py.SoftLink, h5py.ExternalLink)):
            # copy link
            pass
        elif isinstance(sub_obj, h5py.Group):
            copy_group(sub_obj, f_out)
        elif isinstance(sub_obj, h5py.Dataset):
            copy_dataset(sub_obj, f_out)
        else:
            warnings.warn('Unknown h5py object found: %s: %s' % (key, sub_obj))


def copy_dataset(dataset, f_out):
    selection = []
    new_shape = []
    for dim_len in dataset.shape:
        new_dim_len = min(dim_len, MAX_SHAPE_PER_DIM)
        new_shape.append(new_dim_len)
        selection.append(slice(new_dim_len))

    # NOTE this omits compression, compression_opts, scaleoffset, shuffle, fletcher32, fillvalue,
    # track_times, track_order, external, allow_unknown_filter
    new_dataset = f_out.create_dataset(
        name=dataset.name,
        shape=new_shape,
        dtype=dataset.dtype,
        data=dataset.data[selection],  # lazily read only a selection of the dataset
        maxshape=dataset.maxshape,  # will chunk if set to not None using default chunk size
    )
    copy_attributes(dataset, new_dataset)
    # TODO handle dataset of references


def copy_attributes(old_obj, new_obj):
    # NOTE: large attributes will be copied because they are at most 64 KB
    for attr_name, attr_value in old_obj.attrs.items():
        new_obj.attrs[attr_name] = attr_value


if __name__ == '__main__':
    """
    Usage: python nwbtrim.py dir_name
    """
    main()

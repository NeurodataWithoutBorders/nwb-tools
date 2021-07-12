import argparse
import h5py
import os

# maximum length of a scalar string attribute to print
MAX_LEN_STR_PRINT = 120

H5_TEXT = h5py.special_dtype(vlen=str)
H5_BINARY = h5py.special_dtype(vlen=bytes)


def main():
    parser = argparse.ArgumentParser('python nwb_ls.py')
    parser.add_argument('-g', '--group', dest='group', default='/',
                        help='Name of a group to dump the contents of (default: /).')
    parser.add_argument('path', help='Path to an NWB file')
    args = parser.parse_args()

    if not args.path.endswith('.nwb'):
        raise ValueError('Path must point to an NWB file.')

    nwb_ls(args.path, args.group)


def nwb_ls(path, group):
    """Print NWB file metadata.

    Parameters
    ----------
    group : str
        Name of a group to dump the contents of.
    """
    with h5py.File(path, mode='r') as f:
        print_group(f[group])


def print_group(obj, prefix=' ' * 2):
    """Recursively iterate through groups in a HDF5 file and print the names and attributes of the groups and datasets.

    Parameters
    ----------
    prefix : str
        Prefix to append to the printed line at each level of the hierarchy (default: two spaces)
    """
    base_prefix = prefix  # save the base prefix to add to each level

    def _print_sub_obj_helper(obj, prefix):
        """Print a group or dataset and its contents and attributes."""
        if isinstance(obj, h5py.Group):
            for key, sub_obj in obj.items():
                link_type = obj.get(key, getlink=True)
                if isinstance(link_type, (h5py.SoftLink, h5py.ExternalLink)):
                    _print_link(prefix, obj, key, sub_obj, link_type)
                else:
                    _print_sub_obj(prefix, key, sub_obj)
                    _print_sub_obj_helper(obj[key], prefix=prefix + base_prefix)
        if isinstance(obj, (h5py.Group, h5py.Dataset)):
            for key, attr in obj.attrs.items():
                _print_attr(prefix, obj, key, attr)

    _print_sub_obj_helper(obj, '')


def _print_link(prefix, obj, key, sub_obj, link_type):
    if isinstance(sub_obj, h5py.Group):
        linked_obj_type = 'Group'
    else:
        linked_obj_type = 'Dataset'
    if isinstance(link_type, h5py.SoftLink):
        obj_str = 'Soft Link to %s at %s' % (linked_obj_type, link_type.path)
    else:
        # external links are stored as relative file paths so print the relative path
        rel_path = os.path.relpath(sub_obj.file.filename, os.path.dirname(obj.file.filename))
        obj_str = 'External Link to %s at %s://%s' % (linked_obj_type, rel_path, link_type.path)
    print(prefix + '- ' + key + ':', obj_str)


def _print_sub_obj(prefix, key, sub_obj):
    if isinstance(sub_obj, h5py.Group):
        obj_str = 'Group (%d members)' % len(sub_obj)
    elif isinstance(sub_obj, h5py.Dataset):
        if sub_obj.shape == ():  # scalar dataset
            if sub_obj.dtype == H5_TEXT:
                dtype = 'str'
                dset_value = sub_obj.asstr()[()]
            elif sub_obj.dtype == H5_BINARY:
                dtype = 'bytes'
                dset_value = sub_obj[()]
            else:
                dtype = str(sub_obj.dtype)
                dset_value = sub_obj[()]
            if not (isinstance(dset_value, (str, bytes)) and len(dset_value) > MAX_LEN_STR_PRINT):
                # do not print value of long string scalar
                obj_str = 'Dataset (shape: (), type: %s, value: %s)' % (dtype, dset_value)
            else:
                obj_str = 'Dataset (shape: (), type: %s, length: %d)' % (dtype, len(dset_value))
        else:
            if sub_obj.dtype == H5_TEXT:
                dtype = 'str'
            elif sub_obj.dtype == H5_BINARY:
                dtype = 'bytes'
            else:
                dtype = str(sub_obj.dtype)
            obj_str = 'Dataset (shape: %s, dtype: %s)' % (str(sub_obj.shape), dtype)
    else:
        obj_str = sub_obj
    print(prefix + '- ' + key + ':', obj_str)


def _print_attr(prefix, obj, key, attr):
    if isinstance(attr, h5py.Reference):
        attr_str = 'Reference to %s' % obj.file[attr].name
    elif hasattr(attr, 'shape') and attr.shape > ():  # non-scalar attribute
        attr_str = 'Attribute (shape: %s, dtype: %s)' % (str(attr.shape), str(attr.dtype))
    elif isinstance(attr, (str, bytes)) and len(attr) > MAX_LEN_STR_PRINT:  # long string scalar
        attr_str = 'Attribute (shape: (), type: %s, length: %d)' % (str(type(attr)), len(attr))
    else:
        attr_str = attr
    print(prefix + '> ' + key + ':', attr_str)


if __name__ == '__main__':
    main()

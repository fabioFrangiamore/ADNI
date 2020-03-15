from __future__ import print_function, division
import logging
import os


import ants


logger = logging.getLogger(__name__)

def preprocess(img_path, out_dir, mask_path=None, res=(1,1,1), orientation='RAI', n4_opts=None):
    """
    preprocess.py MR images according to a simple scheme,
    that is:
        1) N4 bias field correction
        2) resample to 1mm x 1mm x 1mm
        3) reorient images to RAI
    Args:
        img_dir (str): path to directory containing images
        out_dir (str): path to directory for output preprocessed files
        mask_dir (str): path to directory containing masks
        res (tuple): resolution for resampling (default: (1,1,1) in mm
        n4_opts (dict): n4 processing options (default: None)
    Returns:
        None, outputs preprocessed images to file in given out_dir
    """

    if n4_opts is None:
        n4_opts = {'iters': [200, 200, 200, 200], 'tol': 0.0005}
    logger.debug('N4 Options are: {}'.format(n4_opts))

    # get and check the images and masks
    img_fns = img_path
    mask_fns = mask_path

    # create the output directory structure
    out_img_dir = os.path.join(out_dir, 'imgs')
    out_mask_dir = os.path.join(out_dir, 'masks')
    if not os.path.exists(out_dir):
        logger.info('Making output directory structure: {}'.format(out_dir))
        os.mkdir(out_dir)
    if not os.path.exists(out_img_dir):
        logger.info('Making image output directory: {}'.format(out_img_dir))
        os.mkdir(out_img_dir)
    if not os.path.exists(out_mask_dir) and mask_path is not None:
        logger.info('Making mask output directory: {}'.format(out_mask_dir))
        os.mkdir(out_mask_dir)

    # preprocess the images by n4 correction, resampling, and reorientation

    _, img_base, img_ext = split_filename(img_fns)
    #logger.info('Preprocessing image: {} ({:d}/{:d})'.format(img_base, i, len(img_fns)))

    img = ants.image_read(img_fns)
    if mask_path is not None:
        _, mask_base, mask_ext = split_filename(mask_fns)
        mask = ants.image_read(mask_fns)
        smoothed_mask = ants.smooth_image(mask, 1)
        # this should be a second n4 after an initial n4 (and coregistration), once masks are obtained
        img = ants.n4_bias_field_correction(img, convergence=n4_opts, weight_mask=smoothed_mask)

        out_mask = os.path.join(out_mask_dir, mask_base + mask_ext)
        ants.image_write(mask, out_mask)
    else:
        img = ants.n4_bias_field_correction(img, convergence=n4_opts)
    if hasattr(img, 'reorient_image2'):
        img = img.reorient_image2(orientation)
    else:
        logger.info('Cannot reorient image to a custom orientation. Update ANTsPy to a version >= 0.1.5.')
        img = img.reorient_image((1,0,0))['reoimage']
    out_img = os.path.join(out_img_dir, img_base + img_ext)
    ants.image_write(img, out_img)



from glob import glob
import os

import nibabel as nib


def split_filename(filepath):
    """ split a filepath into the full path, filename, and extension (works with .nii.gz) """
    path = os.path.dirname(filepath)
    filename = os.path.basename(filepath)
    base, ext = os.path.splitext(filename)
    if ext == '.gz':
        base, ext2 = os.path.splitext(base)
        ext = ext2 + ext
    return path, base, ext


def open_nii(filepath):
    """ open a nifti file with nibabel and return the object """
    image = os.path.abspath(os.path.expanduser(filepath))
    obj = nib.load(image)
    return obj


def save_nii(obj, outfile, data=None, is_nii=False):
    """ save a nifti object """
    if not is_nii:
        if data is None:
            data = obj.get_data()
        nib.Nifti1Image(data, obj.affine, obj.header)\
            .to_filename(outfile)
    else:
        obj.to_filename(outfile)


def glob_nii(dir):
    """ return a sorted list of nifti files for a given directory """
    fns = sorted(glob(os.path.join(dir, '*.nii*')))
    return fns
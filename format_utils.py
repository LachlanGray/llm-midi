def find_bin_with_dict(velocity):
    """
    Find the bin number for a given MIDI velocity using a dictionary.

    Args:
    velocity (int): The MIDI velocity.

    Returns:
    int: The bin number corresponding to the velocity.
    """
    # Hardcoded bin thresholds
    bin_thresholds = [0, 1, 2, 3, 5, 6, 8, 11, 15, 21, 28, 38, 51, 69, 94, 127]
    mapping = {
        0: 0,
        1: 1,
        2: 2,
        3: 3,
        4: 4,
        5: 5,
        6: 6,
        7: 6,
        8: 7,
        9: 7,
        10: 7,
        11: 8,
        12: 8,
        13: 8,
        14: 8,
        15: 9,
        16: 9,
        17: 9,
        18: 9,
        19: 9,
        20: 9,
        21: 10,
        22: 10,
        23: 10,
        24: 10,
        25: 10,
        26: 10,
        27: 10,
        28: 11,
        29: 11,
        30: 11,
        31: 11,
        32: 11,
        33: 11,
        34: 11,
        35: 11,
        36: 11,
        37: 11,
        38: 12,
        39: 12,
        40: 12,
        41: 12,
        42: 12,
        43: 12,
        44: 12,
        45: 12,
        46: 12,
        47: 12,
        48: 12,
        49: 12,
        50: 12,
        51: 13,
        52: 13,
        53: 13,
        54: 13,
        55: 13,
        56: 13,
        57: 13,
        58: 13,
        59: 13,
        60: 13,
        61: 13,
        62: 13,
        63: 13,
        64: 13,
        65: 13,
        66: 13,
        67: 13,
        68: 13,
        69: 14,

    }


    # # Create a dictionary mapping velocity ranges to bin numbers
    # velocity_bins = {}
    # for i in range(len(bin_thresholds) - 1):
    #     velocity_bins[(bin_thresholds[i], bin_thresholds[i + 1])] = i

    # # Find and return the corresponding bin number
    # for (low, high), bin_num in velocity_bins.items():
    #     if low <= velocity < high:
    #         return bin_num

    # return len(bin_thresholds) - 2  # In case the velocity is the maximum (127)


# Test the updated function with some sample velocities
# sample_velocities = [0, 30, 60, 90, 127]
# bin_assignments_dict = [find_bin_with_dict(velocity) for velocity in sample_velocities]
# bin_assignments_dict


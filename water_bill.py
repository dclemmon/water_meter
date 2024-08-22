#! /usr/bin/env python3

import argparse
import pathlib

from datetime import datetime

import yaml


class Reading:
    def __init__(self, timestamp, model, mid, consumption, leak, leaknow):
        """
        Build a meter reading instance
        """
        self.timestamp = datetime.fromisoformat(timestamp)
        self.model = model
        self.meter_id = mid
        self.consumption = consumption
        self.leak = leak
        self.leaknow = leaknow

    @classmethod
    def from_dict(cls, raw_dict):
        """
        Create a reading instance from a raw dict
        """
        reading = cls(
                timestamp=raw_dict.get("time"),
                model=raw_dict.get("model"),
                mid=raw_dict.get("id"),
                consumption=raw_dict.get("consumption"),
                leak=raw_dict.get("leak"),
                leaknow=raw_dict.get("leaknow"),
                )
        return reading

    def __eq__(self, other):
        """
        Check if readings are the same
        """
        return self.__dict__ == other.__dict__


def load_readings_from_json(record_path):
    """
    Load the readings from a file
    """
    try:
        import json
    except ImportError as e:
        print(f"Error importing JSON: {e.message}")
    with open(record_path, 'r') as f:
        data = [json.loads(x) for x in f.readlines()]
    return [Reading.from_dict(x) for x in data]


def load_config_from_yaml(config_path):
    """
    Load the configuration from file
    """
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config


def parse_args():
    """
    Parse command line args
    """
    parser = argparse.ArgumentParser(description='View Water Bill Breakdown')
    parser.add_argument('-t', '--readingtype', default='json')
    parser.add_argument('-f', '--file', type=pathlib.Path)
    parser.add_argument('-c', '--config', type=pathlib.Path, default=None)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    # try and load our file by extension
    suffix = args.file.suffix.strip('.')
    loader = locals().get(f"load_readings_from_{suffix}", lambda x: (_ for _ in ()).throw(RuntimeError("Unsupported File Type")))
    readings = loader(args.file)
    config = load_config_from_yaml(args.config.as_posix()) if args.config else {}


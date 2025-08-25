import argparse
import yaml
import json
from pathlib import Path
from datetime import datetime
from experiment import Experiment


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()
    
    with open(args.config) as f:
        config = yaml.safe_load(f)
    
    experiment = Experiment(config)
    results = experiment.run_samples()
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_dir = Path(f"logs/{timestamp}")
    log_dir.mkdir(parents=True, exist_ok=True)
    
    with open(log_dir / "transcript.json", "w") as f:
        json.dump(results, f, indent=2)
    
    with open(log_dir / "config.yaml", "w") as f:
        yaml.dump(config, f)
    
    print(f"Results saved to: {log_dir}")


if __name__ == "__main__":
    main()
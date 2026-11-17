# Cryptic Signal Core

Shared ROS 2 message definitions and text encoding for AGi systems. The package provides typed `NeuralImpulse` and `TelepathicSignal` messages, plus a lossless UTF-8 codec for compact signal payloads.

## Package

- ROS package: `cryptic_signal_core`
- Message types: `cryptic_signal_core.msg.NeuralImpulse`, `cryptic_signal_core.msg.TelepathicSignal`
- Python codec: `cryptic_signal_core.telepathic_encoding`
- Requires ROS 2 Jazzy, `ament_cmake`, `rosidl_default_generators`, and `builtin_interfaces`.

## Build

Add this repository to a ROS 2 workspace alongside the packages that depend on it, then run:

```sh
source /opt/ros/jazzy/setup.bash
colcon build --packages-up-to cryptic_signal_core
source install/setup.bash
```

## License

AGPL-3.0-only. See [LICENSE](LICENSE).

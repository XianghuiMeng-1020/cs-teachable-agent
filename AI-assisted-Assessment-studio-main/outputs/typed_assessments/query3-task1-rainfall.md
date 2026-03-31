# Rainfall Problem seeded by Science Fiction

- Item ID: `task_1-rainfall`
- Item Type: `rainfall`
- Source Task: `task_1`
- Source Path: `/Volumes/T7/idea/pytasksyn/outputs/query_3/task_1`

## Prompt
In the Science Fiction monitoring log, sensors report rainfall readings as floats in the order they were entered. Implement `average_valid_readings(readings)` so it scans the list from left to right, stops at the sentinel -999.0, ignores any other negative value, and returns the average of the valid non-negative readings seen before the sentinel. If no valid readings are seen before the sentinel, return 0.0.

## Interaction Content
In the Science Fiction monitoring log, sensors report rainfall readings as floats in the order they were entered. Implement `average_valid_readings(readings)` so it scans the list from left to right, stops at the sentinel -999.0, ignores any other negative value, and returns the average of the valid non-negative readings seen before the sentinel. If no valid readings are seen before the sentinel, return 0.0.

- Function: `average_valid_readings`
- Sentinel: `-999.0`
- Input Rule: `readings` is a list of floats in the exact order received from the sensor log.
- Filter Rule: Ignore negative readings except for the sentinel itself.

### Public Tests
- `basic_average`: input=[10.0, 20.0, 30.0, -999.0], expected=20.0
- `ignore_invalid_negative`: input=[8.0, -2.0, 4.0, -999.0], expected=6.0
- `stop_at_sentinel`: input=[5.0, 15.0, -999.0, 40.0], expected=10.0

## Answer Key
```json
{
  "function_name": "average_valid_readings",
  "sentinel": -999.0,
  "expected_behavior": "Average all valid non-negative readings before the sentinel and return 0.0 if there are none."
}
```

## Grading Rule
Score by executing the submitted function against the public and hidden tests; full credit requires all tests to pass.

## Validation
- Passed: `True`
- warning: Rainfall item uses a theme-seeded template fallback rather than a direct transformation of the source task.
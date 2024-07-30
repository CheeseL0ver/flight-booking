# Desciption
Sample application to create flight reservations. Application features the following requirements:

The state of reserved seats should be maintained in a file
- A given seat cannot be reserved by more than one person
- Once a person has a seat reservation they cannot be moved
- If a customer cancels their reservation, the seat is available for reserving again
- If a customer wants to reserve multiple seats together in the same row, we should be able to accommodate that or tell the customer it’s not possible
- Must be able to run in a Linux environment
- Input must be accepted from CLI arguments specifically
- Input will be in the format of [Action] [Starting Seat] [Number of consecutive seats]
           - Expected usage:
              - $ ./<file_name> BOOK A1 1

- Output must go to STDOUT
   - Output must only be in the format of “SUCCESS” or “FAIL”
- Any expected/unexpected errors should not go to STDOUT
- This should not be an interactive terminal. It must be a command-line driven input. Example:
   - Expected usage:
     - $ ./<file_name> BOOK A1 1
       SUCCESS
     - $ ./<file_name> CANCEL A1 1
       SUCCESS

# Requirements
- Python >=3.8 

# Usage

```bash
$ sudo chmod +x ./app
$ ./app BOOK A1 1 #SUCCESS
$ ./app CANCEL A1 1 #SUCCESS

$ ./app BOOK A1 1 #SUCCESS
$ ./app BOOK A1 1 #FAIL
```

> Note: Verbose logging can be enabled by using the `-v` flag.

> Note: To run all of the given test cases, the `runner.sh` script can be used:
```bash
$ sudo chmod +x ./runner.sh
$ ./runner.sh
```

# Additonal Notes/Considerations

- Prevented use of external Python dependencies to prevent overhead and display
  core Python knowledge.

- Used Python's `pickle` module as there was no direct requirement to have the data in the file be human-readable and using `pickle` allowed me to save my custom `Data` class directly, which I believe made the logic of the code easier to follow

- "Saved" on quite a bit of logic by taking full advantage of regular expressions
  for the "command" processing logic. Regular expressions have been a large part of
  the work I have done in my current role and I hope to see more regular expression
  make their way into code bases as exposure creates familiarity (at least that has been
  my experience).

- Used verbose type hints to aid in code readbility. In the project I currently
  lead I would be lost without them, definietly an under appreciated feature by some. 


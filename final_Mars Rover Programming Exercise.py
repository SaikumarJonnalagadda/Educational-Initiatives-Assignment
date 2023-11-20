from enum import Enum

# Enum for directions
class Direction(Enum):
    NORTH = 'N'
    EAST = 'E'
    SOUTH = 'S'
    WEST = 'W'

# Command interface for Command Pattern based on SOLID principles
# for each command i have created a class such that each class executes only one command like move,turnleft,turnRight
class Command:
    def execute(self, rover):
        #Execute the command on the given Rover.
        pass

# Concrete commands
class Move(Command):
    def execute(self, rover):
        #Execute the move command on the Rover.
        return rover.move()

class TurnLeft(Command):
    def execute(self, rover):
        #Execute the turn left command on the Rover.
        rover.turn_left()

class TurnRight(Command):
    def execute(self, rover):
        #Execute the turn right command on the Rover.
        rover.turn_right()

# Custom exception for obstacle detection
class ObstacleDetectedException(Exception):
    pass

# Receiver class for Rover which creates instances of Rover based on commands and updates the position
class Rover:
    def __init__(self, x, y, direction, grid_size, obstacles):
        #Initialize the Rover with its starting position and constraints.
        self.x = x
        self.y = y
        self.direction = Direction(direction)
        self.grid_size = grid_size
        self.obstacles = obstacles
        self.obstacle_report = "No obstacles detected"

    def move(self):
        #Move the Rover to its next position if the move is valid.
        new_x, new_y = self.calculate_new_position()
        if self.is_valid_move(new_x, new_y):
            self.x, self.y = new_x, new_y
        else:
            raise ObstacleDetectedException("Obstacle detected. Rover cannot move.")

    def turn_left(self):
        #Turn the Rover left.
        directions = list(Direction)
        current_index = directions.index(self.direction)
        self.direction = directions[(current_index - 1) % len(directions)]

    def turn_right(self):
        #Turn the Rover right.
        directions = list(Direction)
        current_index = directions.index(self.direction)
        self.direction = directions[(current_index + 1) % len(directions)]

    def calculate_new_position(self):
        #Calculate the new position based on the current direction
        if self.direction == Direction.NORTH:
            return self.x, self.y + 1
        elif self.direction == Direction.SOUTH:
            return self.x, self.y - 1
        elif self.direction == Direction.EAST:
            return self.x + 1, self.y
        elif self.direction == Direction.WEST:
            return self.x - 1, self.y

    def is_valid_move(self, new_x, new_y):
        #Check if the new position is a valid move within the grid and not an obstacle.
        return 0 <= new_x < self.grid_size[0] and 0 <= new_y < self.grid_size[1] and (new_x, new_y) not in self.obstacles

    def status_report(self):
        #Generate a status report for the Rover.
        return f"Rover is at ({self.x}, {self.y}) facing {self.direction.name}. {self.obstacle_report}."

    def final_position(self):
        #Get the final position of the Rover.
        return f"Final Position: ({self.x}, {self.y}, {self.direction.name})"

# Command Parser class for parsing command strings into a list of command objects
class CommandParser:
    @staticmethod
    def parse(command_str):
        #Parse a string of commands and return a list of corresponding command objects.
        commands = []
        for char in command_str:
            if char == 'M':
                commands.append(Move())
            elif char == 'L':
                commands.append(TurnLeft())
            elif char == 'R':
                commands.append(TurnRight())
            else:
                print(f"The command {char} is not in my command prompt")
        return commands

# Client class for Command Pattern where it takes the command and executes the command given in the input
class RoverController:
    def __init__(self, rover):
        #Initialize the RoverController with a Rover instance and an empty list of commands.
        self.rover = rover
        self.commands = []

    def add_command(self, command_str):
        #Add commands to the list using the CommandParser.
        parsed_commands = CommandParser.parse(command_str)
        self.commands.extend(parsed_commands)

    def execute_commands(self):
        #Execute each command in the list on the Rover.
        for command in self.commands:
            try:
                command.execute(self.rover)
            except ObstacleDetectedException as e:
                print(e)
                break

if __name__ == "__main__":
    # Define grid size, starting position, and obstacles based on given input
    grid_size = (10, 10)
    starting_position = (0, 0, 'N')
    obstacles = [(2, 2), (3, 5)]

    # Initialize Rover
    rover = Rover(*starting_position, grid_size, obstacles)

    # Initialize Controller with Rover
    controller = RoverController(rover)
    commands = ['M','M','R','M','L','M']

    # Add commands
    controller.add_command(commands)

    # Execute commands
    controller.execute_commands()

    # Final position
    print(rover.final_position())

    # Display status report
    print(rover.status_report())

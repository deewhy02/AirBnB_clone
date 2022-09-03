#!/usr/bin/python3
"""
AirBnB clone command interpreter
"""
import cmd
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State


def parse(arg):
    """Helper method to parse user typed input"""
    return tuple(arg.split())


class HBNBCommand(cmd.Cmd):
    """
    HBNB command interpreter
    """
    intro = "Welcome to ALX AirBnB clone command interpreter"
    prompt = "(hbnb) "
    class_dict = {"BaseModel", "State", "City",
                  "Amenity", "Place", "Review", "User"}

    def do_EOF(self, line):
        """Ctrl-D to quit program"""
        print()
        return True

    def do_quit(self, line):
        """Quit command to exit program"""
        return True

    def emptyline(self):
        """Overwrite default behavior to repeat last cmd"""
        pass

    def do_create(self, user_arg):
        """Create instance specified by user"""
        if len(user_arg) == 0:
            print("** class name missing **")
        elif user_arg not in HBNBCommand.class_dict:
            print("** class doesn't exist **")
        else:
            instance = eval(user_arg)()
            instance.save()
            print(instance.id)

    def do_show(self, user_arg):
        """Print string repr of a class instance, given id"""
        args = parse(user_arg)
        obj_dict = storage.all()
        if len(user_arg) == 0:
            print("** class name missing **")
        elif args[0] not in HBNBCommand.class_dict:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(args[0], args[1]) not in obj_dict:
            print("** no instance found **")
        else:
            print(obj_dict["{}.{}".format(args[0], args[1])])

    def do_destroy(self, user_arg):
        """Delete a class instance of a given id, save result to json file."""
        args = parse(user_arg)
        obj_dict = storage.all()
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in HBNBCommand.class_dict:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(args[0], args[1]) not in obj_dict.keys():
            print("** no instance found **")
        else:
            del obj_dict["{}.{}".format(args[0], args[1])]
            storage.save()

    def do_all(self, user_arg):
        """Prints all string representation of all instances based or
        not on the class name"""
        args = parse(user_arg)
        obj_dict = storage.all()
        obj_list = []
        if len(args) > 0 and args[0] in HBNBCommand.class_dict:
            for objs in obj_dict.values():
                if len(args) > 0 and args[0] == objs.__class__.__name__:
                    obj_list.append(objs.__str__())
                elif len(args) == 0:
                    obj_list.append(objs.__str__())
            print(obj_list)
        else:
            print("** class doesn't exist **")

    def do_update(self, user_arg):
        """Updates an instance based on the class name and id by adding
            or updating attribute (save the change into the JSON file)"""
        args = parse(user_arg)
        obj_dict = storage.all()
        if len(args) >= 4:
            key = "{}.{}".format(args[0], args[1])
            cast = type(eval(args[3]))
            arg3 = args[3]
            arg3 = arg3.strip('"')
            arg3 = arg3.strip("'")
            setattr(obj_dict[key], args[2], cast(arg3))
            obj_dict[key].save()
        elif len(args) == 0:
            print("** class name missing **")
        elif args[0] not in HBNBCommand.class_dict:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        elif ("{}.{}".format(args[0], args[1])) not in obj_dict.keys():
            print("** no instance found **")
        elif len(args) == 2:
            print("** attribute name missing **")
        else:
            print("** value missing **")

    def do_count(self, user_arg):
        """Display count of instances specified"""
        if user_arg in HBNBCommand.class_dict:
            count = 0
            for key, value in storage.all().items():
                if user_arg in key:
                    count += 1
            print(count)
        else:
            print("** class doesn't exist **")

    def default(self, user_arg):
        """Use  class name and command arguement to display class instances"""
        args = user_arg.split('.')
        class_arg = args[0]
        if len(args) == 1:
            print("*** Unknown syntax: {}".format(user_arg))
            return
        try:
            args = args[1].split('(')
            command = args[0]
            """ stripping braces around id """
            arg = args[1].split(")")
            id_arg = arg[0]
            id_arg = id_arg.strip("'")
            id_arg = id_arg.strip('"')
            ids = class_arg + " " + id_arg

            if command == 'all':
                HBNBCommand.do_all(self, class_arg)
            elif command == 'count':
                HBNBCommand.do_count(self, class_arg)
            elif command == 'show':
                HBNBCommand.do_show(self, ids)
            elif command == 'destroy':
                HBNBCommand.do_destroy(self, ids)
            elif command == 'update':
                args = args[1].split(',')
                id_arg = args[0].strip("'")
                id_arg = id_arg.strip('"')
                # name_arg = args[1].strip(',')
                # val_arg = args[2]
                # name_arg = name_arg.strip(' ')
                # name_arg = name_arg.strip("'")
                # name_arg = name_arg.strip('"')
                # val_arg = val_arg.strip(' ')
                # val_arg = val_arg.strip(')')
                if type(eval(args[1])) is dict:
                    for key, value in args[1].items():
                        args[1] = args[1].split(",")
                        args[1] = args[1].strip(' ')
                        args[1] = args[1].strip("}")
                        name_arg = key.strip('"')
                        name_arg = key.strip("'")
                        name_arg = key.split(":")
                        val_arg = value.strip('"')
                        val_arg = value.strip("'")
                        # name_arg = key.strip("{")
                        val_arg = value.strip(")")
                else:
                    # args = args[1].split(',')
                    # id_arg = args[0].strip("'")
                    # id_arg = id_arg.strip('"')
                    name_arg = args[1].strip(',')
                    val_arg = args[2]
                    name_arg = name_arg.strip(' ')
                    name_arg = name_arg.strip("'")
                    name_arg = name_arg.strip('"')
                    val_arg = val_arg.strip(' ')
                    val_arg = val_arg.strip(')')
                arg = class_arg + ' ' + id_arg + ' ' + name_arg + ' ' + val_arg
                HBNBCommand.do_update(self, arg)
            else:
                print("*** Unknown syntax: {}".format(user_arg))
        except IndexError:
            print("*** Unknown syntax: {}".format(user_arg))


if __name__ == '__main__':
    HBNBCommand().cmdloop()

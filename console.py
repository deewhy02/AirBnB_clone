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
    # intro = "Welcome to ALX AirBnB clone command interpreter"
    prompt = "(hbnb) "
    class_dict = {"BaseModel", "State", "City",
                  "Amenity", "Place", "Review", "User"}

    def do_EOF(self, line):
        return True

    def help_EOF(self):
        print("EOF signal to exit the program\n")

    def do_quit(self, line):
        return True

    def help_quit(self):
        print("Quit command to exit the program\n")

    def emptyline(self):
        """Overwrite default behavior to repeat last cmd"""
        pass

    def do_create(self, user_arg):
        if len(user_arg) == 0:
            print("** class name missing **")
        elif user_arg not in HBNBCommand.class_dict:
            print("** class doesn't exist **")
        else:
            instance = eval(user_arg)()
            instance.save()
            print(instance.id)

    def help_create(self):
        print("Create instance specified by user\n")

    def do_show(self, user_arg):
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

    def help_show(self):
        print("Print string repr of a class instance, given id\n")

    def do_destroy(self, user_arg):
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

    def help_destroy(self):
        print("Delete a class instance of a given id,", end="")
        print(" save result to json file\n")

    def do_all(self, user_arg):
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

    def help_all(self):
        print("Prints all string representation of all instances", end="")
        print(" based or not on the class name\n")

    """def do_update(self, user_arg):
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
            print("** value missing **")"""

    def do_update(self, arg):
        argl = parse(arg)
        objdict = storage.all()

        if len(argl) == 0:
            print("** class name missing **")
            return False
        if argl[0] not in HBNBCommand.class_dict:
            print("** class doesn't exist **")
            return False
        if len(argl) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(argl[0], argl[1]) not in objdict.keys():
            print("** no instance found **")
            return False
        if len(argl) == 2:
            print("** attribute name missing **")
            return False
        if len(argl) == 3:
            try:
                type(eval(argl[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(argl) == 4:
            obj = objdict["{}.{}".format(argl[0], argl[1])]
            if argl[2] in obj.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__[argl[2]])
                obj.__dict__[argl[2]] = valtype(argl[3])
            else:
                obj.__dict__[argl[2]] = argl[3]
        elif type(eval(argl[2])) == dict:
            obj = objdict["{}.{}".format(argl[0], argl[1])]
            for k, v in eval(argl[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    valtype = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = valtype(v)
                else:
                    obj.__dict__[k] = v
        storage.save()

    def help_update(self):
        print("Updates an instance based on the class name and id by", end="")
        print(" adding or updating attribute", end="")
        print(" (save the change into the JSON file)\n")

    def do_count(self, user_arg):
        if user_arg in HBNBCommand.class_dict:
            count = 0
            for key, value in storage.all().items():
                if user_arg in key:
                    count += 1
            print(count)
        else:
            print("** class doesn't exist **")

    def help_count(self):
        print("Display count of instances specified\n")

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
                name_arg = args[1].strip(',')
                val_arg = args[2]
                name_arg = name_arg.strip(' ')
                name_arg = name_arg.strip("'")
                name_arg = name_arg.strip('"')
                val_arg = val_arg.strip(' ')
                val_arg = val_arg.strip(')')
                """if type(eval(args[1])) is dict:
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
                    val_arg = val_arg.strip(')')"""
                arg = class_arg + ' ' + id_arg + ' ' + name_arg + ' ' + val_arg
                HBNBCommand.do_update(self, arg)
            else:
                print("*** Unknown syntax: {}".format(user_arg))
        except IndexError:
            print("*** Unknown syntax: {}".format(user_arg))


if __name__ == '__main__':
    HBNBCommand().cmdloop()

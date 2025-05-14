class citizen:

    def leave(self):
        return "leave DOA"
    

class mollacDAO_citizen(citizen):

    def leave(self):
        return "rage quit"
    

if __name__ == "__main__":

    citizen1 = citizen()
    citizen2 = mollacDAO_citizen()

    print(citizen1.leave())
    print(citizen2.leave())

    print(issubclass(mollacDAO_citizen, citizen))

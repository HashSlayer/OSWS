# Define a base class named 'Citizen'
class Citizen:
    """
    A class representing a generic citizen.
    
    Methods
    -------
    leave():
        Returns a string indicating the citizen's action when leaving.
    """
    
    def leave(self):
        """
        Simulate the action of leaving.
        
        Returns
        -------
        str
            A message indicating the citizen's departure.
        """
        return "leave DOA"  # Default leave message for a generic citizen
    

# Define a subclass named 'MollacDAOCitizen' that inherits from 'Citizen'
class MollacDAOCitizen(Citizen):
    """
    A class representing a citizen of the MollacDAO, inheriting from Citizen.
    
    Methods
    -------
    leave():
        Overrides the leave method to provide a specific message for MollacDAO citizens.
    """
    
    def leave(self):
        """
        Simulate the action of leaving with a specific message for MollacDAO citizens.
        
        Returns
        -------
        str
            A message indicating the citizen's departure in a unique manner.
        """
        return "rage quit"  # Specific leave message for a MollacDAO citizen
    

# Main execution block to demonstrate class usage
if __name__ == "__main__":
    # Create an instance of the Citizen class
    citizen1 = Citizen()
    # Create an instance of the MollacDAOCitizen class
    citizen2 = MollacDAOCitizen()

    # Call the leave method on both instances and print the results
    print(citizen1.leave())  # Output: leave DOA
    print(citizen2.leave())  # Output: rage quit

    # Check if MollacDAOCitizen is a subclass of Citizen
    print(issubclass(MollacDAOCitizen, Citizen))  # Output: True

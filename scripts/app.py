from app.parking import add_vehicle, vehicle_exit, show_parking_status
from app.receipts import generate_receipt

def main():
    while True:
        print("\n Vehicle Parking System")
        print("1. Park a vehicle")
        print("2. Exit a vehicle")
        print("3. Show parking status")
        print("4. Generate receipt")
        print("5. Exit program")
        choice = input("Enter choice: ")
        
        if choice == "1":
            vehicle_number = input("Enter vehicle number: ")
            vehicle_type = input("Enter vehicle type (Car/Bike): ")
            add_vehicle(vehicle_number, vehicle_type)
        elif choice == "2":
            vehicle_number = input("Enter vehicle slot number: ")
            vehicle_exit(vehicle_number)
        elif choice == "3":
            show_parking_status()
        elif choice == "4":
            vehicle_number = input("Enter exited vehicle slot number: ")
            generate_receipt(vehicle_number)
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
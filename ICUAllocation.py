class ICUAllocation:
    def __init__(self, total_beds):
        self.total_beds = total_beds
        self.available_beds = total_beds
        self.patients = {}
        self.waiting_list = []

    def calculate_priority(self, age, oxygen, heart_rate,
                           blood_pressure, temperature, condition):
        score = 0

        # Oxygen level
        if oxygen < 90:
            score += 30
        elif oxygen < 94:
            score += 20

        # Heart rate
        if heart_rate > 120 or heart_rate < 50:
            score += 20
        elif heart_rate > 100 or heart_rate < 60:
            score += 10

        # Blood pressure (systolic)
        if blood_pressure < 90:
            score += 20
        elif blood_pressure < 100:
            score += 10

        # Temperature
        if temperature >= 39 or temperature <= 35:
            score += 15
        elif temperature >= 38:
            score += 10

        # Age
        if age >= 65:
            score += 10

        # Existing medical condition
        if condition.strip().lower() not in ["none", "no", ""]:
            score += 5

        return score

    def classify_patient(self, score):
        if score >= 70:
            return "CRITICAL"
        elif score >= 50:
            return "HIGH"
        elif score >= 30:
            return "MEDIUM"
        else:
            return "LOW"

    def add_patient(self, patient_id, age, oxygen, heart_rate,
                    blood_pressure, temperature, condition,
                    emergency=False):

        # Duplicate patient ID
        if patient_id in self.patients:
            return "ERROR: Duplicate patient ID."

        # Input validation
        if oxygen < 0 or oxygen > 100:
            return "ERROR: Invalid oxygen level."

        if heart_rate <= 0:
            return "ERROR: Invalid heart rate."

        if age < 0:
            return "ERROR: Invalid age."

        score = self.calculate_priority(
            age,
            oxygen,
            heart_rate,
            blood_pressure,
            temperature,
            condition
        )

        priority = self.classify_patient(score)

        patient = {
            "id": patient_id,
            "age": age,
            "oxygen": oxygen,
            "heart_rate": heart_rate,
            "blood_pressure": blood_pressure,
            "temperature": temperature,
            "condition": condition,
            "score": score,
            "priority": priority,
            "emergency": emergency,
            "bed": False
        }

        self.patients[patient_id] = patient

        # Emergency cases override normal allocation
        if emergency:
            if self.available_beds > 0:
                self.available_beds -= 1
                patient["bed"] = True
                return "EMERGENCY: ICU bed allocated."

            else:
                # Emergency goes to front of waiting list
                self.waiting_list.insert(0, patient_id)
                return "EMERGENCY: No ICU bed available. Patient placed first on waiting list."

        # Normal allocation
        if self.available_beds > 0:
            self.available_beds -= 1
            patient["bed"] = True
            return f"ICU bed allocated. Priority: {priority}"

        # No beds
        self.waiting_list.append(patient_id)
        return f"No ICU bed available. Patient placed on waiting list. Priority: {priority}"

    def get_patient(self, patient_id):
        if patient_id not in self.patients:
            return "ERROR: Patient not found."

        return self.patients[patient_id]

    def allocate_waiting_patients(self):
        if self.available_beds <= 0:
            return "No ICU beds available."

        # Sort:
        # 1. Emergency first
        # 2. Higher priority score first
        self.waiting_list.sort(
            key=lambda pid: (
                self.patients[pid]["emergency"],
                self.patients[pid]["score"]
            ),
            reverse=True
        )

        allocated = []

        while self.available_beds > 0 and self.waiting_list:
            patient_id = self.waiting_list.pop(0)

            patient = self.patients[patient_id]
            patient["bed"] = True

            self.available_beds -= 1
            allocated.append(patient_id)

        return allocated

    def get_waiting_list(self):
        return self.waiting_list

    def get_available_beds(self):
        return self.available_beds


# -------------------------------
# Main Program
# -------------------------------

if __name__ == "__main__":

    print("=== ICU RESOURCE ALLOCATION SYSTEM ===")

    beds = int(input("Enter number of ICU beds: "))

    system = ICUAllocation(beds)

    patient_id = input("Patient ID: ")
    age = int(input("Age: "))
    oxygen = float(input("Oxygen level: "))
    heart_rate = int(input("Heart rate: "))
    blood_pressure = int(input("Blood pressure (systolic): "))
    temperature = float(input("Temperature: "))
    condition = input("Existing medical condition: ")

    emergency_input = input("Emergency case? (yes/no): ")
    emergency = emergency_input.lower() == "yes"

    result = system.add_patient(
        patient_id,
        age,
        oxygen,
        heart_rate,
        blood_pressure,
        temperature,
        condition,
        emergency
    )

    print("\nResult:", result)

    patient = system.get_patient(patient_id)

    if isinstance(patient, dict):
        print("Priority Score:", patient["score"])
        print("Priority:", patient["priority"])
        print("ICU Bed:", "Allocated" if patient["bed"] else "Not Allocated")

    print("Available ICU beds:", system.get_available_beds())
    print("Waiting List:", system.get_waiting_list())

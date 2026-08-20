class ICUAllocation:

    def __init__(self, total_beds):
        self.total_beds = total_beds
        self.available_beds = total_beds
        self.patients = {}
        self.waiting_list = []

    def calculate_priority(self, age, oxygen_level, heart_rate,
                           blood_pressure, temperature, medical_condition):

        score = 0

        # Oxygen level
        if oxygen_level < 90:
            score += 30
        elif oxygen_level < 94:
            score += 20
        elif oxygen_level < 96:
            score += 10

        # Heart rate
        if heart_rate > 120 or heart_rate < 50:
            score += 20
        elif heart_rate > 100 or heart_rate < 60:
            score += 10

        # Blood pressure - systolic
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
        if medical_condition.lower() not in ["none", "no", ""]:
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

    def add_patient(self, patient_id, age, oxygen_level,
                    heart_rate, blood_pressure, temperature,
                    medical_condition, emergency=False):

        # Duplicate patient ID
        if patient_id in self.patients:
            return "ERROR: Duplicate patient ID."

        # Validate age
        if age < 0:
            return "ERROR: Invalid age."

        # Validate oxygen
        if oxygen_level < 0 or oxygen_level > 100:
            return "ERROR: Invalid oxygen level."

        # Validate heart rate
        if heart_rate <= 0:
            return "ERROR: Invalid heart rate."

        # Calculate priority
        score = self.calculate_priority(
            age,
            oxygen_level,
            heart_rate,
            blood_pressure,
            temperature,
            medical_condition
        )

        priority = self.classify_patient(score)

        patient = {
            "id": patient_id,
            "age": age,
            "oxygen_level": oxygen_level,
            "heart_rate": heart_rate,
            "blood_pressure": blood_pressure,
            "temperature": temperature,
            "medical_condition": medical_condition,
            "score": score,
            "priority": priority,
            "emergency": emergency,
            "bed_allocated": False
        }

        self.patients[patient_id] = patient

        # Allocate bed if available
        if self.available_beds > 0:

            self.available_beds -= 1
            patient["bed_allocated"] = True

            if emergency:
                return "EMERGENCY: ICU bed allocated."

            return "ICU bed allocated."

        # No beds available
        if emergency:
            # Emergency patients go to the front
            self.waiting_list.insert(0, patient_id)
            return "EMERGENCY: No bed available. Patient placed first on waiting list."

        self.waiting_list.append(patient_id)

        return "No ICU bed available. Patient placed on waiting list."

    def get_patient(self, patient_id):

        if patient_id not in self.patients:
            return None

        return self.patients[patient_id]

    def get_available_beds(self):
        return self.available_beds

    def get_waiting_list(self):
        return self.waiting_list

    def allocate_waiting_patients(self):

        if self.available_beds <= 0:
            return []

        # Emergency first, then highest priority score
        self.waiting_list.sort(
            key=lambda patient_id: (
                self.patients[patient_id]["emergency"],
                self.patients[patient_id]["score"]
            ),
            reverse=True
        )

        allocated = []

        while self.available_beds > 0 and len(self.waiting_list) > 0:

            patient_id = self.waiting_list.pop(0)

            patient = self.patients[patient_id]

            patient["bed_allocated"] = True

            self.available_beds -= 1

            allocated.append(patient_id)

        return allocated

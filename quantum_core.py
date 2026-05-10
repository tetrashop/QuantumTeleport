"""هسته کوانتومی: شبیه‌ساز دقیق کیوبیت و پروتکل دورنورد"""
import math, random, time
from typing import List, Tuple

# ماتریس‌های پایه
PAULI_X = [[0,1],[1,0]]
PAULI_Z = [[1,0],[0,-1]]
HADAMARD = [[1/math.sqrt(2), 1/math.sqrt(2)],
            [1/math.sqrt(2), -1/math.sqrt(2)]]

class QuantumRegister:
    """ثبات n-کیوبیتی با بردار حالت"""
    def __init__(self, n: int):
        self.n = n
        self.state = [0] * (2**n)
        self.state[0] = 1.0  # شروع از |00...0>

    def apply_gate(self, gate, target: int):
        """اعمال گیت تک‌کیوبیتی روی کیوبیت target"""
        new_state = [0] * len(self.state)
        for i, amp in enumerate(self.state):
            if amp == 0:
                continue
            b0 = (i >> target) & 1
            mask = ~(1 << target)
            base = i & mask
            for b in (0,1):
                new_idx = base | (b << target)
                new_state[new_idx] += amp * gate[b][b0]
        self.state = new_state

    def apply_cnot(self, control: int, target: int):
        """CNOT: اگر کنترل 1 باشد هدف را می‌زند"""
        new_state = [0] * len(self.state)
        for i, amp in enumerate(self.state):
            if amp == 0:
                continue
            c = (i >> control) & 1
            t = (i >> target) & 1
            if c == 1:
                t_flipped = 1 - t
            else:
                t_flipped = t
            new_idx = i ^ ( (t ^ t_flipped) << target )
            new_state[new_idx] += amp
        self.state = new_state

    def measure(self, target: int) -> int:
        """اندازه‌گیری محاسباتی یک کیوبیت و فروپاشی"""
        prob0 = sum(abs(amp)**2 for i, amp in enumerate(self.state) if ((i >> target) & 1) == 0)
        if random.random() < prob0:
            result = 0
        else:
            result = 1
        # فروپاشی
        norm = 0
        for i, amp in enumerate(self.state):
            if ((i >> target) & 1) != result:
                self.state[i] = 0
            else:
                norm += abs(amp)**2
        if norm > 0:
            factor = 1/math.sqrt(norm)
            for i in range(len(self.state)):
                self.state[i] *= factor
        return result

    def get_qubit_state(self, idx: int):
        """استخراج حالت یک کیوبیت جداگانه (پس از جداسازی)"""
        prob0 = sum(abs(self.state[i])**2 for i in range(len(self.state)) if ((i >> idx) & 1) == 0)
        prob1 = 1 - prob0
        # تخمین فاز ساده‌سازی شده برای دو سطح
        state0, state1 = 0+0j, 0+0j
        for i, amp in enumerate(self.state):
            if ((i >> idx) & 1) == 0:
                state0 += amp
            else:
                state1 += amp
        norm = math.sqrt(abs(state0)**2 + abs(state1)**2)
        if norm == 0:
            return (1+0j, 0+0j)
        return (state0/norm, state1/norm)

class Qubit:
    """کیوبیت منفرد برای حالت اولیه"""
    def __init__(self, alpha: complex = 1, beta: complex = 0):
        norm = math.sqrt(abs(alpha)**2 + abs(beta)**2)
        self.alpha = alpha/norm
        self.beta = beta/norm

class QuantumTeleportProtocol:
    """پروتکل صحیح دورنوردی با شبیه‌سازی سه‌کیوبیتی"""
    def teleport(self, psi: Qubit) -> Qubit:
        # ایجاد ثبت 3 کیوبیتی: psi (index 0), alice (1), bob (2)
        reg = QuantumRegister(3)
        # آماده‌سازی حالت psi روی کیوبیت 0
        # ابتدا صفر است -> باید α|0⟩+β|1⟩ کنیم
        reg.state[0] = psi.alpha
        reg.state[1] = psi.beta  # حالت |001>? دقت: کیوبیت 0 بیت کم‌اهمیت
        # بهتر: بر اساس نگاشت: index = q2 q1 q0 (بیت 0 برای کیوبیت 0)
        # پس حالت psi.alpha|000> + psi.beta|001> را می‌خواهیم:
        reg.state[0] = psi.alpha   # |000>
        reg.state[1] = psi.beta    # |001>
        # بقیه صفر
        # ایجاد جفت بل: هادامارد روی alice (q1)، سپس CNOT(q1, q2)
        reg.apply_gate(HADAMARD, 1)
        reg.apply_cnot(1, 2)
        # پروتکل: CNOT(psi, alice) -> کنترل psi=0، هدف alice=1
        reg.apply_cnot(0, 1)
        # هادامارد روی psi
        reg.apply_gate(HADAMARD, 0)
        # اندازه‌گیری psi و alice
        m0 = reg.measure(0)  # اندازه‌گیری psi
        m1 = reg.measure(1)  # اندازه‌گیری alice
        # تصحیح روی bob (q2)
        if m1 == 1:  # اگر alice 1 بود، X روی bob
            reg.apply_gate(PAULI_X, 2)
        if m0 == 1:  # اگر psi 1 بود، Z روی bob
            reg.apply_gate(PAULI_Z, 2)
        # استخراج حالت bob
        bob_alpha, bob_beta = reg.get_qubit_state(2)
        return Qubit(bob_alpha, bob_beta)

class AdvancedMatterTeleporter:
    def __init__(self):
        self.efficiency = 0.95
    def teleport_element(self, z, energy_per_nucleon=1.5e-10):
        from atomic_data import PERIODIC_TABLE
        if z not in PERIODIC_TABLE:
            return None
        sym, name, mass, _ = PERIODIC_TABLE[z]
        nucleons = round(mass)
        ideal = nucleons * energy_per_nucleon
        real = ideal / self.efficiency
        time.sleep(0.01 * math.log(nucleons+1))
        return real, f"Advanced teleport {name}: {real:.2e} J"

"""موتور دورنوردی ماده بر اساس داده‌های اتمی"""
import math
import time
from atomic_data import PERIODIC_TABLE, ANTI_TABLE

class MatterScanner:
    @staticmethod
    def scan_element(z: int) -> dict:
        if z not in PERIODIC_TABLE:
            raise ValueError(f"عنصر {z} موجود نیست")
        sym, name, mass, config = PERIODIC_TABLE[z]
        return {'z': z, 'symbol': sym, 'name': name, 'atomic_mass': mass,
                'electron_config': config, 'num_nucleons': round(mass)}

    @staticmethod
    def scan_molecule(formula: str) -> dict:
        # تحلیل ساده فرمول (H2O, CO2, ...)
        atoms = {}
        i = 0
        while i < len(formula):
            sym = formula[i]
            i += 1
            while i < len(formula) and formula[i].islower():
                sym += formula[i]
                i += 1
            count = 0
            while i < len(formula) and formula[i].isdigit():
                count = count * 10 + int(formula[i])
                i += 1
            if count == 0:
                count = 1
            atoms[sym] = atoms.get(sym, 0) + count
        total_mass = 0.0
        result = {'formula': formula, 'atoms': []}
        for sym, cnt in atoms.items():
            z = None
            for num, (s, _, _, _) in PERIODIC_TABLE.items():
                if s == sym:
                    z = num
                    break
            if z is None:
                raise ValueError(f"نماد ناشناخته: {sym}")
            _, name, mass, _ = PERIODIC_TABLE[z]
            result['atoms'].append({'z': z, 'symbol': sym, 'count': cnt, 'mass_per_atom': mass, 'name': name})
            total_mass += mass * cnt
        result['total_mass'] = total_mass
        return result

class QuantumTeleporter:
    def __init__(self):
        self.energy_per_nucleon = 1.5e-10  # ژول

    def teleport_element(self, z: int, use_antimatter=False):
        table = ANTI_TABLE if use_antimatter else PERIODIC_TABLE
        if z not in table:
            return None
        sym, name, mass, _ = table[z]
        nucleons = round(mass)
        energy = nucleons * self.energy_per_nucleon
        time.sleep(0.02)
        prefix = "ضد" if use_antimatter else ""
        return f"دورنورد {prefix}عنصر {name} ({sym}) | نوکلئون‌ها: {nucleons} | انرژی: {energy:.2e} J"

    def teleport_molecule(self, formula: str):
        scanner = MatterScanner()
        mol = scanner.scan_molecule(formula)
        total_energy = 0.0
        report = f"مولکول {formula}:\n"
        for atom in mol['atoms']:
            e = atom['count'] * round(atom['mass_per_atom']) * self.energy_per_nucleon
            total_energy += e
            report += f"  {atom['count']}×{atom['name']} ({atom['symbol']}) - جرم کل: {atom['count']*atom['mass_per_atom']:.2f} u\n"
        report += f"انرژی کل: {total_energy:.2e} J\n✅ بازسازی موفق"
        return report

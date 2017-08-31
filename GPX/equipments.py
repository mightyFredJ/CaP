# encoding utf8

import sys
import doctest

# %% -------------------------------------------------------------------

known_equipments = [
    '<EquipmentItem Id="a9c3e7b0-a185-46d3-b35d-3d0216b34ae2" Name="Asics - Trabuco 12 WR" />',
    '<EquipmentItem Id="b8c19522-5b18-4a4e-b1aa-c5f5835d48ad" Name="Asics - GT 2130 old" />',
    '<EquipmentItem Id="52baf2aa-1ee2-434d-b564-1028b72c7d07" Name="Asics - GT 2140" />',
    '<EquipmentItem Id="d087de10-6a97-4f94-8c04-b9cb74d6bc14" Name="Asics - GT 2140-2" />',
    '<EquipmentItem Id="39d601f6-7b36-45a4-9547-441a7e5c43d5" Name="Asics - GT-2150" />',
    '<EquipmentItem Id="72d359f2-0f16-4aff-9534-e44c126c8dd1" Name="Asics - Trabuco II" />',
    '<EquipmentItem Id="26b75913-ff6f-4542-adfe-c95fb2a2abb0" Name="Asics - Trabuco 3" />',
    '<EquipmentItem Id="f6a34d4c-e471-4eab-a399-cc8ae9520133" Name="Kalenji - Kapteren quickdry" />',
    '<EquipmentItem Id="461e0fce-0698-44a8-b44a-2f75f09d178f" Name="Kalenji - Kapteren TR3" />',
    '<EquipmentItem Id="827424ed-9b13-42ce-a28d-2cef48763efa" Name="Kalenji - XT3" />',
    '<EquipmentItem Id="014dff4b-2f74-48f8-afa5-81166e30d5e8" Name="Rockrider - SàD 5 L" />',
    '<EquipmentItem Id="3df18cc7-50a5-4ead-8597-49995117cc8a" Name="Petzl - Myo XP" />',
    '<EquipmentItem Id="6b8795f9-99b7-4e08-a0c3-ed51c64628c0" Name="Quechua - Bâtons" />',

    '<EquipmentItem Id="63e6815d-effe-40d2-a991-7a24da3a1057" Name="Adidas - Kanadia" />',
    '<EquipmentItem Id="7e0c988b-4abc-4ce8-83b1-ea660616de29" Name="Adidas - Kanadia 2" />',
    '<EquipmentItem Id="0b2c100f-9160-45c8-a1e7-f171e6afa83a" Name="Armytek - Wizard V3" />',
    '<EquipmentItem Id="6344f300-60e9-4bba-9f57-0d29f7df27a1" Name="Asics - Fuji Trabuco 3" />',
    '<EquipmentItem Id="b719ff7c-4ffc-4a25-a27a-0f08e5668992" Name="Asics - Fuji Trabuco 3 (2)" />',
    '<EquipmentItem Id="2cda837f-c73f-4c32-a9c6-116e81eecb94" Name="Asics - Fuji Trabuco 3 II" />',
    '<EquipmentItem Id="85e7f6e4-d27f-408f-8800-bb67cbf8d18b" Name="Asics - Fuji Trainer 3" />',
    '<EquipmentItem Id="05ac9ab6-3649-4ccf-b3fb-21b91a8a1bce" Name="Asics - Gel-Pulse 6" />',
    '<EquipmentItem Id="6e08ed39-dce7-4c2d-a31f-b5f800f5a7e6" Name="Asics - Tambora 2" />',
    '<EquipmentItem Id="d627b7d5-c513-4aa7-9c5b-3b8e303b6fec" Name="Kalenji - Inspid" />',
    '<EquipmentItem Id="0bad1ac6-fc8c-4221-be07-6c0ac3b222fb" Name="Kalenji - Guêtres" />',
    '<EquipmentItem Id="132de178-8f0a-4746-8f75-0c084e44484c" Name="Kalenji - Kiprun" />',
    '<EquipmentItem Id="e2fdc25e-0fd3-411a-a35f-471ab1d79f6c" Name="Kalenji - Kiprace" />',
    '<EquipmentItem Id="f0d6f9cc-6de8-4678-8cde-07ed97faffd8" Name="Kalenji - OnNight 410v2" />',
    '<EquipmentItem Id="deac708d-ce8f-456c-9d9c-268f49d74c93" Name="Quechua - SàD Diosaz Raid 17" />',
    '<EquipmentItem Id="653f522c-01ba-4874-bd94-08240ec50752" Name="Quechua - SàD 2-12L" />',
    '<EquipmentItem Id="2f554cb7-cb21-431b-b61e-b32dae6cb70b" Name="Quechua - SàD MT 20L" />',
    '<EquipmentItem Id="fbd24382-8aca-4745-8b8d-d13da6b0cfcb" Name="Quechua - Bâtons 2" />',
    '<EquipmentItem Id="0ffda5a3-ffbe-4cf8-bb15-90799b82a948" Name="Raidlight - Guêtres" />',
    '<EquipmentItem Id="0700723c-ec47-418c-9547-4daa13e1363a" Name="Raidlight - Guêtres 2" />',
    '<EquipmentItem Id="82010298-3336-48fd-9204-52044157b874" Name="Ronhill - Tempest" />',
]

# ----------------------------------------------------------------

def get_equipment(substring, case_sensitive = False):
    """
        >>> print(get_equipment('truc'))
        <!-- no equipment matched 'truc' -->
        
        >>> print(get_equipment('Armytek'))
        <EquipmentItem Id="0b2c100f-9160-45c8-a1e7-f171e6afa83a" Name="Armytek - Wizard V3" />
        
        >>> print(get_equipment('kip'))
        <!-- 2 equipments matched 'kip' :                                                
        <EquipmentItem Id="132de178-8f0a-4746-8f75-0c084e44484c" Name="Kalenji - Kiprun" />  
        <EquipmentItem Id="e2fdc25e-0fd3-411a-a35f-471ab1d79f6c" Name="Kalenji - Kiprace" /> 
        -->                                                                                  
    """
    matched = []
    for equ in known_equipments:
        if case_sensitive is True:
            if substring in equ:
                matched.append(equ)
        else:
            if substring.lower() in equ.lower():
                matched.append(equ)
    
    retour = None
    if len(matched) == 1:
        retour = matched[0]
    elif len(matched) == 0:
        retour = "<!-- no equipment matched '%s' -->" % substring
    else:
        retour = "<!-- %d equipments matched '%s' :\n" % (len(matched), substring)
        retour += "\n".join([e for e in matched])
        retour += "\n-->"
    
    return retour

# %% -------------------------------------------------------------------

if __name__ == "__main__":
    quiet = len(sys.argv) > 1 and '-q' in sys.argv[1]
    if quiet:
        sys.stdout = io.StringIO()

    # ---- do the tests
    opts = doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE
    (fails, tests) = doctest.testmod(optionflags=opts)
    # ---- done

    sys.stdout = sys.__stdout__  # même si not quiet ça ne coûte rien

    if tests == 0:
        print('no tests in this file')
    elif tests > 0 and fails == 0:  # sinon pas d'affichage c'est pénible
        print('%d tests successfully passed' % tests)
    elif quiet:
        print('%d tests over %d FAILED' % (fails, tests))

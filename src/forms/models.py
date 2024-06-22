from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

DISCIPLINE_DICT = {
    "Water":
    [
        "Flow",
        "Stance",
        "Ice",
        "Steam",
        "Blood",
        "Body",
    ],
    "Earth":
    [
        "Terraform",
        "Mud",
        "Projectiles",
        "Defense",
        "Sand",
        "Metal",
        "Lava",
        "Seismic Sense",
    ],
    "Fire": 
    [
        "Strikes",
        "Projectiles",
        "Defense",
        "Lightning",
        "Heat Control",
    ],
    "Air":
    [
        "Air Ball",
        "Blast",
        "Flight",
        "Swirl",
        "Wind",
        "Detect",
        "Projection",
        "Vacuum",
    ]
}

MASTERY_LEVELS = [
    "Novice",
    "Intermediate",
    "Advanced",
    "Master",
    "Multi-Master",
    "Depends",
    "N/A"
]

DND_CLASSES =  [
    "Barbarian",
    "Bard",
    "Cleric",
    "Druid",
    "Fighter",
    "Monk",
    "Paladin",
    "Ranger",
    "Rogue",
    "Sorcerer",
    "Warlock",
    "Wizard",
]

DND_ABILITIES = [
    "Strength",
    "Dexterity",
    "Constitution",
    "Intelligence",
    "Wisdom",
    "Charisma",
]

DND_SKILLS = [
    "Acrobatics",
    "Animal Handling",
    "Arcana",
    "Athletics",
    "Deception",
    "History",
    "Insight",
    "Intimidation",
    "Investigation",
    "Medicine",
    "Nature",
    "Perception",
    "Performance",
    "Persuasion",
    "Religion",
    "Sleight of Hand",
    "Stealth",
    "Survival"
]

DND_DAMAGE_TYPES = [
    "Acid",
    "Bludgeoning",
    "Cold",
    "Fire",
    "Force",
    "Lightning",
    "Necrotic",
    "Piercing",
    "Poison",
    "Psychic",
    "Radiant",
    "Slashing",
    "Thunder",
    "Healing",
]

COMPONENTS = [
    "Arms",
    "Legs",
    "Mouth",
    "Head",
    "Limb",
    "Digit",
    "Mind",
]

COMBAT_DEFENSES = [
    "Melee",
    "Ranged",
]

ELEMENTS = DISCIPLINE_DICT.keys()
DISCIPLINES = [disc for discipline_list in DISCIPLINE_DICT.values() for disc in discipline_list]

class BaseModel(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class DndCombatDefense(BaseModel):
    name = models.CharField(max_length=20, primary_key=True)

    def __str__(self):
        return f"{self.name}"

class DndClass(BaseModel):
    name = models.CharField(max_length=20, primary_key=True)

    def __str__(self):
        return f"{self.name}"

class DndAbility(DndCombatDefense):
    pass

class DndSkill(DndCombatDefense):
    pass

class DndMasteryLevel(BaseModel):
    name = models.CharField(max_length=20, primary_key=True)

    def __str__(self):
        return f"{self.name}"

class DndCastingSpeed(BaseModel):
    name = models.CharField(max_length=10, primary_key=True)   

    def __str__(self):
        return f"{self.name}"

class DndComponent(BaseModel):
    name = models.CharField(max_length=20, primary_key=True)

    def __str__(self):
        return f"{self.name}"

class DndDamageType(BaseModel):
    name = models.CharField(max_length=20, primary_key=True)
    description = models.TextField()

    def __str__(self):
        return f"{self.name}"
    
class DndElement(BaseModel):
    name = models.CharField(max_length=10, primary_key=True)
    general_desc = models.TextField()
    trait_desc = models.TextField()
    combat_desc = models.TextField()

    def __str__(self):
        return f"{self.name}"

class DndDiscipline(BaseModel):
    name = models.CharField(max_length=20)
    element = models.ForeignKey(DndElement, on_delete=models.CASCADE)
    description = models.TextField()

    class Meta:
        unique_together = ('name', 'element')

    def __str__(self):
        return f"{self.name} ({self.element})"

class DndForm(BaseModel):
    name = models.CharField(max_length=200)
    element = models.ForeignKey(DndElement, on_delete=models.CASCADE)
    discipline = models.ManyToManyField(DndDiscipline)
    mastery = models.ForeignKey(DndMasteryLevel, on_delete=models.CASCADE)
    description = models.TextField()
    has_higher_level_bonus = models.BooleanField()
    higher_levels = models.TextField(blank=True)
    concentration = models.BooleanField()
    target = models.CharField(max_length=20)
    casting_speed = models.ManyToManyField(DndCastingSpeed)
    duration = models.CharField(max_length=20)
    # range = models.CharField(max_length=30)
    # components = models.ManyToManyField(DndComponent)
    saving_throws = models.ManyToManyField(DndCombatDefense)
    classes = models.ManyToManyField(DndClass)
    costs_slot = models.BooleanField()
    special_reqs = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name}"

class DndRoll(BaseModel):
    damage_type = models.ForeignKey(DndDamageType, on_delete=models.CASCADE)
    form = models.ForeignKey(DndForm, on_delete=models.CASCADE)
    num_dice = models.IntegerField()
    num_sides = models.IntegerField()

    def __str__(self):
        return f"{self.num_dice}d{self.num_sides} {self.damage_type} ({self.form})"


edition_definition_dict = {
    DndClass: DND_CLASSES,
    DndAbility: DND_ABILITIES,
    DndElement: ELEMENTS,
    DndMasteryLevel: MASTERY_LEVELS,
    DndDamageType: DND_DAMAGE_TYPES,
    DndComponent: COMPONENTS,
    DndCombatDefense: COMBAT_DEFENSES,
    DndSkill: DND_SKILLS,
}
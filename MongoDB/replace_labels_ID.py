### Replace the labels annotation with unique IDs in the place of same English and French label 
### This file used in the MonggoDB Shell 
### Paste the same code in the MongDB Shell 

db["wastes_copy"].find()
const labelMap = {
    "spent solvents": 0,
    "solvants usés": 0,
    "acid, alkaline or saline wastes": 1,
    "déchets acides, alcalins ou salins": 1,
    "used oils": 2,
    "huiles usées": 2,
    "spent chemical catalysts": 3,
    "catalyseurs chimiques usés": 3,
    "chemical preparation wastes": 4,
    "déchets de préparations chimiques": 4,
    "chemical deposits and residues": 5,
    "dépôts et résidus chimiques": 5,
    "industrial effluent sludges": 6,
    "boues d'effluents industriels": 6,
    "sludges and liquid wastes from waste treatment": 7,
    "boues et déchets liquides du traitement des déchets": 7,
    "health care and biological wastes": 8,
    "déchets de soins de santé et biologiques": 8,
    "metal waste, ferrous": 9,
    "déchets métalliques, ferreux": 9,
    "metal waste, non-ferrous": 10,
    "déchets métalliques, non ferreux": 10,
    "metal wastes, mixed ferrous and non-ferrous": 11,
    "déchets métalliques mixtes, ferreux et non ferreux": 11,
    "glass wastes": 12,
    "déchets de verre": 12,
    "paper and cardboard wastes": 13,
    "déchets de papier et de carton": 13,
    "rubber wastes": 14,
    "déchets de caoutchouc": 14,
    "plastic wastes": 15,
    "déchets plastiques": 15,
    "wood wastes": 16,
    "déchets de bois": 16,
    "textile wastes": 17,
    "déchets textiles": 17,
    "waste containing pcb": 18,
    "déchets contenant des pcb": 18,
    "discarded equipment": 19,
    "équipements mis au rebut": 19,
    "discarded vehicles": 20,
    "véhicules mis au rebut": 20,
    "batteries and accumulators wastes": 21,
    "déchets de batteries et d'accumulateurs": 21,
    "animal and mixed food waste": 22,
    "déchets alimentaires et animaux mélangés": 22,
    "vegetal wastes": 23,
    "déchets végétaux": 23,
    "slurry and manure": 24,
    "boues et fumier": 24,
    "household and similar wastes": 25,
    "déchets ménagers et similaires": 25,
    "mixed and undifferentiated materials": 26,
    "matériaux mélangés et indifférenciés": 26,
    "sorting residues": 27,
    "résidus de tri": 27,
    "common sludges": 28,
    "boues communes": 28,
    "construction and demolition wastes": 29,
    "déchets de construction et de démolition": 29,
    "asbestos waste": 30,
    "déchets d'amiante": 30,
    "waste of naturally occurring minerals": 31,
    "déchets de minéraux naturels": 31,
    "combustion wastes": 32,
    "déchets de combustion": 32,
    "various mineral wastes": 33,
    "divers déchets minéraux": 33,
    "soils": 34,
    "sols": 34,
    "dredging spoil": 35,
    "déblais de dragage": 35,
    "waste from waste treatment": 36,
    "déchets provenant du traitement des déchets": 36,
    "solidified, stabilised or vitrified waste": 37,
    "déchets solidifiés, stabilisés ou vitrifiés": 37
};

// Function to find the closest match by checking for partial (minor) matches
function findClosestMatch(label) {
    const normalizedLabel = label.toLowerCase().trim();
    
    // First, check for a direct match in the labelMap
    if (labelMap.hasOwnProperty(normalizedLabel)) {
        return labelMap[normalizedLabel];
    }

    // Next, check for partial (minor) match
    for (const [key, id] of Object.entries(labelMap)) {
        if (normalizedLabel.includes(key) || key.includes(normalizedLabel)) {
            return id;
        }
    }

    // No match found, return -1
    return -1;
}

// Process each document and update annotations
db.getCollection("wastes_copy").find().forEach(doc => {
    if (doc.annotations && Array.isArray(doc.annotations.annotations)) {
        const updatedAnnotations = doc.annotations.annotations.map(annotation => {
            const originalLabel = (typeof annotation.label === 'string' ? annotation.label : "").trim().toLowerCase();

            // Assign -1 for empty, "unknown," or "inconnu" labels
            if (!originalLabel || originalLabel === "unknown" || originalLabel === "inconnu") {
                annotation.label = -1;
            } else {
                // Find the closest match for the label
                const closestMatchId = findClosestMatch(originalLabel);
                annotation.label = closestMatchId;
            }
            return annotation;
        });

        // Update the document in the collection
        db.getCollection("wastes_copy").updateOne(
            { _id: doc._id },
            { $set: { "annotations.annotations": updatedAnnotations } }
        );
    }
});

print("All annotations labels have been updated with unique IDs or set to -1 for unmatched labels.");

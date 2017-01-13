function Ploidy(config) {
  this._config = config;
  this._description = this._normalize(this._config.ploidyDesc);
}

// Get number of chromosomes in a chromosome set
Ploidy.prototype.getChromosomesNumber = function(setNumber) {
  if (this._config.ploidyDesc) {
    var chrSetCode = this._config.ploidyDesc[setNumber];
    if (chrSetCode instanceof Object) {
      return Object.keys(chrSetCode)[0].length;
    } else {
      return chrSetCode.length;
    }
  } else {
    return this._config.ploidy || 1;
  }
};

// Normalize use defined description
Ploidy.prototype._normalize = function(description) {
    // Return the same if no description provided
  if (!description) {
    return description;
  }

    // Array of normalized description objects
  var normalized = [];

     // Loop through description and normalize
  for (var key in description) {
    if (typeof description[key] === 'string') {
      normalized.push({
        ancestors: description[key],
        existence: this._getexistenceArray(description[key].length)
      });
    } else {
      normalized.push({
        ancestors: Object.keys(description[key])[0],
        existence: description[key][Object.keys(description[key])[0]]
      });
    }
  }

  return normalized;
};

// Get array filled by '11' elements
Ploidy.prototype._getexistenceArray = function(length) {
  var array = [];

  for (var i = 0; i < length; i++) {
    array.push('11');
  }

  return array;
};

Ploidy.prototype.getSetSize = function(chrSetNumber) {
  if (this._description) {
    return this._description[chrSetNumber].ancestors.length;
  } else {
    return 1;
  }
};

// Get ancestor letter
Ploidy.prototype.getAncestor = function(chrSetNumber, chrNumber) {
  if (this._description) {
    return this._description[chrSetNumber].ancestors[chrNumber];
  } else {
    return '';
  }
};

// Check if chromosome's arm should be rendered.
// If no description was provided, method returns true and
// something another depending on user provided description.
Ploidy.prototype.exists = function(chrSetNumber, chrNumber, armNumber) {
  if (this._description) {
    return Number(this._description[chrSetNumber].existence[chrNumber][armNumber]) > 0;
  } else {
    return true;
  }
};

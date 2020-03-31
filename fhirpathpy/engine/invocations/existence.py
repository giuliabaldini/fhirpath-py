import json
import fhirpathpy.engine.util as util
import fhirpathpy.engine.invocations.filtering as filtering

"""
This file holds code to hande the FHIRPath Existence functions 
(5.1 in the specification).
"""


def emptyFn(value):
    return util.isEmpty(value)


def countFn(value):
    if isinstance(value, list):
        return len(value)
    return 0


def notFn(x):
    if len(x) != 1:
        return []

    data = util.valData(x[0])

    if type(data) == bool:
        return not data

    return []


def existsMacro(coll, expr):
    vec = coll
    if expr:
        return existsMacro(filtering.whereMacro(coll, expr))

    return util.isEmpty(vec)


def allMacro(coll, expr):
    for i in range(0, coll):
        if not util.isTrue(expr(coll[i])):
            return [False]

    return [True]


"""
def _assertType(data, types, errorMsgPrefix):
  val = this.valData(data)
  if (types.indexOf(typeof val) < 0):
    let typeList = types.length > 1 ? "one of "+types.join(", ") : types[0];
    util.raiseError("Found type '"+(typeof data)+"' but was expecting " +
      typeList, errorMsgPrefix)
  return val


def allTrueFn(x):
  let rtn = true;
  for (let i=0, len=x.length; i<len && rtn; ++i):
    let xi = util.assertType(x[i], ["boolean"], "allTrue");
    rtn = xi == true;
  }
  return [rtn];


def anyTrueFn(x):
  let rtn = false;
  for (let i=0, len=x.length; i<len && !rtn; ++i):
    let xi = util.assertType(x[i], ["boolean"], "anyTrue");
    rtn = xi == true;
  }
  return [rtn];
};

def allFalseFn(x):
  let rtn = true;
  for (let i=0, len=x.length; i<len && rtn; ++i):
    let xi = util.assertType(x[i], ["boolean"], "allFalse");
    rtn = xi == false;
  }
  return [rtn];
};

def anyFalseFn(x):
  let rtn = false;
  for (let i=0, len=x.length; i<len && !rtn; ++i):
    let xi = util.assertType(x[i], ["boolean"], "anyFalse");
    rtn = xi == false;
  }
  return [rtn];
};


/**
 *  Returns a JSON version of the given object, but with keys of the object in
 *  sorted order (or at least a stable order).
 *  From: https://stackoverflow.com/a/35810961/360782
 */
function orderedJsonStringify(obj):
  return JSON.stringify(sortObjByKey(obj));
}

/**
 *  If given value is an object, returns a new object with the properties added
 *  in sorted order, and handles nested objects.  Otherwise, returns the given
 *  value.
 *  From: https://stackoverflow.com/a/35810961/360782
 */
function sortObjByKey(value):
  return (typeof value == 'object') ?
    (Array.isArray(value) ?
      value.map(sortObjByKey) :
      Object.keys(value).sort().reduce(
        (o, key) => {
          const v = value[key];
          o[key] = sortObjByKey(v);
          return o;
        }, {})
    ) :
    value;
}


/**
 *  Returns true if coll1 is a subset of coll2.
 */
function subsetOf(coll1, coll2):
  let rtn = coll1.length <= coll2.length;
  if (rtn):
    // This requires a deep-equals comparision of every object in coll1,
    // against each object in coll2.
    // Optimize by building a hashmap of JSON versions of the objects.
    var c2Hash = {};
    for (let p=0, pLen=coll1.length; p<pLen && rtn; ++p):
      let obj1 = util.valData(coll1[p]);
      let obj1Str = orderedJsonStringify(obj1);
      let found = false;
      if (p==0): // c2Hash is not yet built
        for (let i=0, len=coll2.length; i<len; ++i):
          // No early return from this loop, because we're building c2Hash.
          let obj2 = util.valData(coll2[i]);
          let obj2Str = orderedJsonStringify(obj2);
          c2Hash[obj2Str] = obj2;
          found = found || (obj1Str == obj2Str);
        }
      }
      else
        found = !!c2Hash[obj1Str];
      rtn = found;
    }
  }
  return rtn;
}

def subsetOfFn(coll1, coll2):
  return [subsetOf(coll1, coll2)];
};

def supersetOfFn(coll1, coll2):
  return [subsetOf(coll2, coll1)];
};
"""


def distinctFn(x):
    unique = []
    # Since this requires a deep equals, use a hash table (on JSON strings)
    # for efficiency.
    if len(x) > 0:
        uniqueHash = {}
        for i in range(0, len(x)):
            xObj = x[i]
            xStr = json.dumps(xObj)
            if not xStr in uniqueHash:
                unique.append(xObj)
                uniqueHash[xStr] = xObj

    return unique


def isDistinctFn(x):
    return [len(x) == len(distinctFn(x))]
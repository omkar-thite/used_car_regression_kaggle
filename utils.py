def handle_outliers(col, limit=2):
    '''
    Truncate outliers according to limit argument
    Truncate here means set values to 0

    Args:
    col (Series): Column to truncate
    limit (int) : Multiple of standard deviation at which to truncate column

    Returns: 
    (Series): Truncated column 
    '''
    # Copy the column
    x = col.copy()

    # Calculate bounds
    mean = x.mean()
    std_dev = x.std()
    lower_bound = mean - (limit * std_dev)
    upper_bound = mean + (limit * std_dev)

    # Reassign values above or below the bounds
    x[x <= lower_bound] = lower_bound
    x[x >= upper_bound] = upper_bound

    return x

# Categorical
def get_automatic(string):
    string = string.lower()
    if 'a/t' in string or 'automatic' in string or 'at' in string:
        return 1
    else:
        return 0
    
# Categorical
def get_gears(string):
    match = re.search(r'^(\d+)-Speed', string, re.IGNORECASE)
    if match:
        gears = match.group(1)
        return int(gears)
    else:
        return None

# Contiunuos
def get_hp(engine):
    match = re.search(r'([\d.]+)HP', engine, re.IGNORECASE)
    if match:
      return float(match.group(1))
    else:
      return None

# Continuos
def get_L(engine):
    match = re.search(r'([\d.]+)L', engine, re.IGNORECASE)
    if match:
      return float(match.group(1))
    else:
      return None

# Categorical
def get_cyl(engine):
    match = re.search(r'([\d.]+)?\s?(?:Cylinder|Cyl|Cylinders)', engine, re.IGNORECASE)
    if match:
      return int(match.group(1))
    else:
      return None

# Categorical
def is_electric(engine):
    if 'electric' in engine.lower():
      return 1
    else:
      return 0

# Continuos
def num_valves(engine):
    match = re.search(r'([\d+])V', engine)
    if match:
      return float(match.group(1))
    else:
      return None

# Categorical
def is_accident(accident):
    if type(accident) == str:
        if 'accident' in accident.lower():
          return 1
        else:
          return 0
    else:
        return None
                            


# Cleans the categorical and continuos data for missing values using imputation
# try experimeting with median imputer for both continuos and categorical

class Cleaner():
    def __init__(self, df):
      self.df = df
      self.categoricals = []
      self.continuos = []
      self.categoricals_imputed = []
      self.continuos_imputed = []

      self.mean_imputer = SimpleImputer(strategy='mean')
      self.mode_imputer = SimpleImputer(strategy='most_frequent')

      self.update_vars()


    def update_vars(self, extra_categoricals=[], extra_continuos=[]):
        '''
        Updates list of categoricals and continuos variables based on dtypes
        Features with dtype int, object and category are considered categoricals while float features are considered continuos.

        Args:
        extra_categoricals (list): Non categorical features which are to be trated as categoricals
        extra_continuos (list) :  Non continuos features to be trated as continuos
        '''
        self.categoricals = list(set(self.categoricals) | set(self.df.select_dtypes(include=[int, object, 'category']).columns))

        if extra_categoricals:
            self.categoricals = list(set(self.categoricals) | set(extra_categoricals))

        self.continuos = [col for col in self.df.columns if col not in self.categoricals]
        if extra_continuos:
            self.continuos = list(set(self.continuos) | set(extra_continuos))


    def clean_categoricals(self):
        '''
        Cleans categorical features using Mode imputation
        '''
        self.update_vars()
        categorical_missing_vars = list(filter(lambda x: x not in self.categoricals_imputed, self.categoricals))

        if categorical_missing_vars:
          print(f'Categorical_missing_vars: {categorical_missing_vars}')
          self.df[categorical_missing_vars] = self.mode_imputer.fit_transform(self.df[categorical_missing_vars])
          self.categoricals_imputed += categorical_missing_vars


    def clean_continuos(self):
        self.update_vars()

        continuos_missing_vars = list(filter(lambda x: x not in self.continuos_imputed, self.continuos))

        if continuos_missing_vars:
          print(f'Continuos_missing_vars: {continuos_missing_vars}')
          self.df[continuos_missing_vars] = self.mean_imputer.fit_transform(self.df[continuos_missing_vars])
          self.continuos_imputed += continuos_missing_vars

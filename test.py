import pandas as pd


options = ["parry", "block", "drive reversal", "dp", "forward jump", "neutral/back jump", "backdash", "jab", "wakeup low", "super"]
outcomes = list("0011101001")
inputs = []
for option in options:
    inputs.append(0)

inputsDF = pd.DataFrame(data={"weights": inputs, "outcomes": outcomes}, index=options)
inputsDF["weights"]["parry"] = 1
inputsDF["weights"]["dp"] = 2
inputsDF["weights"]["super"] = 3
print(x :=inputsDF[inputsDF["weights"] > 0])
# total = sum(x['weights'])
# x['weights'] = x['weights'] / total
print(list(x.index))

# print(inputsDF.gt(0, axis=0))
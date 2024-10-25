from attr import define, field
from eqb.sign_flow_vos.signFlowByFile.Docs import Docs
from eqb.sign_flow_vos.signFlowByFile.SignFlowConfig import SignFlowConfig
from eqb.sign_flow_vos.signFlowByFile.Signers import Signers

@define
class SignFlowByFile():
    
    docs: Docs = field(default= None)

    signFlowConfig: SignFlowConfig = field(default= None)

    signers: Signers = field(default= None)


if __name__ == '__main__':
    signFlowByFile = SignFlowByFile()
    print(signFlowByFile)
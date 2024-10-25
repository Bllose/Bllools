from attr import define, field
from eqb.sign_flow_vos.signers.SignFields import SignField

@define
class Signers():

    # 签署方类型，0 - 个人，1 - 企业/机构，2 - 法定代表人，3 - 经办人
    signerType: str

    _signFields: list[SignField] = field(factory=list)

    @_signFields.validator
    def checkSignFields(self, attributions, value):
        for sign in value:
            if not isinstance(sign, SignField):
                raise ValueError(f"All elements in signFields must be SignField instances, got {type(sign)}")

    @property   
    def signFields(self):
        return self._signFields
    
    @signFields.setter
    def signFields(self, value):
        if all(isinstance(item, SignField) for item in value):
            self._signFields = value
        else :
            raise ValueError('signFields 中所有的参数都必须是SignField!')
            

if __name__ == '__main__':
    signers = Signers(signerType=0)
    signers.signFields = [SignField(fileId='')]
    print(signers)
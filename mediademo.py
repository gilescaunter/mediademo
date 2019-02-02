from troposphere import ec2
from troposphere import Ref
from troposphere import Tags
from troposphere import Join
from troposphere import Base64
from troposphere import Template

from troposphere.s3 import Bucket

everyone = '0.0.0.0/0'

SG_rule = ec2.SecurityGroupRule

ingress = [
    SG_rule(IpProtocol='tcp', FromPort=22, ToPort=22, CidrIp=everyone),
    SG_rule(IpProtocol='tcp', FromPort=80, ToPort=80, CidrIp=everyone),
    SG_rule(IpProtocol='tcp', FromPort=443, ToPort=443, CidrIp=everyone)
]

egress = [SG_rule(IpProtocol='tcp', FromPort=0, ToPort=65535, CidrIp=everyone)]

amazon_linux_SG = ec2.SecurityGroup('AmazonLinuxMachineSG',
                                    VpcId='vpc-cb0bf3af',
                                    GroupDescription='Allow SSH, HTTP and HTTPS',
                                    SecurityGroupIngress=ingress,
                                    SecurityGroupEgress=egress,
                                    Tags=Tags(Name='AmazonLinuxMachine SG',
                                              Application=Ref('AWS::StackName')))

ec2_instance = ec2.Instance('AmazonLinuxMachine',
                            SecurityGroupIds=[Ref(amazon_linux_SG)],
                            KeyName='tutorial-serverless',
                            InstanceType='t2.micro',
                            InstanceInitiatedShutdownBehavior='stop',
                            DisableApiTermination=True,
                            SubnetId='subnet-d9ed25af',
                            Tags=Tags(Name='Amazon Linux Machine',
                                      Application=Ref('AWS::StackId'),
                                      Details='Created by Cloud Formation'),
                            SourceDestCheck=False,
                            ImageId='ami-f9dd458a',

                            UserData=Base64(Join("", [
                                "#!/bin/bash\n",
                                "yum install python27-devel python27-pip gcc",
                                "yum install libjpeg-devel zlib-devel python-pip"
                                "pip install -U pip",
                                "pip install virtualenv"
                            ]))

                            )

tutorial_images = Bucket('ttrserverlessimages', BucketName="ttrserverlessimages")
tutorial_imagescover = Bucket('ttrserverlessimagescover', BucketName="ttrserverlessimagescover")
tutorial_imagesprofile = Bucket('ttrserverlessimagesprofile', BucketName="ttrserverlessimagesprofile")
tutorial_imagesthumbnail = Bucket('ttrserverlessimagesthumbnail', BucketName="ttrserverlessimagesthumbnail")

if __name__ == '__main__':
    template = Template()
    template.add_version('2010-09-09')
    template.add_description('This is the template describing resources required for this tuto setup')

    template.add_resource(amazon_linux_SG)
    template.add_resource(ec2_instance)
    template.add_resource(tutorial_images)
    template.add_resource(tutorial_imagescover)
    template.add_resource(tutorial_imagesprofile)
    template.add_resource(tutorial_imagesthumbnail)

    with open('template.json', 'w') as fd:
        fd.write(template.to_json(indent=4, sort_keys=True))
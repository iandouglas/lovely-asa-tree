import datetime
import json
import random

import bleach
from flask import request
from flask_restful import Resource, abort


def _validate_field(data, field, proceed, errors, missing_okay=False):
    if field in data:
        # sanitize the user input here
        data[field] = bleach.clean(data[field].strip())
        if len(data[field]) == 0:
            proceed = False
            errors.append(f"required '{field}' parameter is blank")
    if not missing_okay and field not in data:
        proceed = False
        errors.append(f"required '{field}' parameter is missing")
        data[field] = ''

    return proceed, data[field], errors


TREES = [
    {
        'name': 'Ellcrys, "The Shannara Chronicles"',
        'description': 'Telepathic, magical elf trees are always pretty rad, but poor Ellcrys tends to get completely overshadowed by all the other white trees in fantasy pop culture, of which there are many.',
        'image_url': 'https://ugc.reveliststatic.com/gen/full/2016/04/27/14/9j/7l/pogmddl0ws39.gif'
    },
    {
        'name': 'The Truffula Trees, "The Lorax"',
        'description': "They're so cool looking, and they make excellent thneeds! Too bad their spokesman isn't very effective at his job and now they're all gone.",
        'image_url': 'https://ugc.reveliststatic.com/gen/full/2016/04/27/14/cf/z9/po33vsou0w39.gif'
    },
    {
        'name': "Toad Tree – Pan's Labyrinth",
        'description': "This being a tree designed by Guillermo del Toro, you won't be surprised to discover it's not the kind of tree you gather your friends beneath to have tea parties. No, the tree in Pan's Labyrinth is a twisted oak that's home to all manner of disgusting bugs and insects, not to mention an over-amorous toad with a key to immortality in its belly. Rule of thumb: If you find any tree in the woods that you can climb inside or scurry beneath, or that contains a portal to a world of mystery, give it a miss. Other trees are available to play in. It might be full of mud and roaches and evil life-sucking toads, but now that Ofelia's cleaned all that mess out it would probably make for a very nice summer home.",
        'image_url': 'https://ugc.reveliststatic.com/gen/constrain/800/800/80/2016/04/27/14/62/co/potzmapgw839.jpg'
    },
    {
        'name': 'The Tree Of Life, "The Lion King"',
        'description': "It's impressive on the outside, but Rafiki's adorable drawings on the inside are what really make it stand out.",
        'image_url': 'https://ugc.reveliststatic.com/gen/constrain/800/800/80/2016/04/27/14/cy/c1/popena46go39.png'
    },
    {
        'name': 'Tree Fort, "Adventure Time"',
        'description': "What's not to love about Jake and Finn's sweet crib? It's full of treasure and video games and bacon pancakes!",
        'image_url': 'https://ugc.reveliststatic.com/gen/constrain/800/800/80/2016/04/27/14/62/61/pojj7e0doo39.png'
    },
    {
        'name': 'The Great Deku Tree, "Legend Of Zelda"',
        'description': 'The only tree on this list who has ever worn a mustache, and boy does he rock it. Ganondorf must be so jealous.',
        'image_url': 'https://ugc.reveliststatic.com/gen/constrain/800/800/80/2016/04/27/14/7m/d2/po8zlb0kso39.jpg'
    },
    {
        'name': 'The "Swiss Family Robinson" Treehouse',
        'description': 'The OG treehouse that every kid wished they could play in but instead had to settle for a plastic jungle gym.',
        'image_url': 'https://ugc.reveliststatic.com/gen/constrain/800/800/80/2016/04/27/14/cw/h1/pozvwzt08c39.jpg'
    },
    {
        'name': 'The Giving Tree',
        'description': "Whether you think it's a beautiful metaphor for motherhood or a terrible metaphor for abusive relationships, you definitely have an opinion about the Giving Tree. It's nice to know that even though she's now a mere stump of her former self, she's still sparking very important discussion.",
        'image_url': 'https://ugc.reveliststatic.com/gen/constrain/800/800/80/2016/04/27/14/1i/6a/po6v3xzu6839.jpg'
    },
    {
        'name': 'The Whomping Willow, "Harry Potter"',
        'description': "Trees are idiots, for the most part – they just sit there sulking while you carve your initials into them and climb all over them. Not the Whomping Willow of Hogwarts – this perennial plant has attitude. Planted in 1971, it hides a secret passage between the school grounds and the Shrieking Shack, and if anyone tries to pass, they get a bloody great branch thwipped to the face – legend has it one Hogwarts student almost lost an eye trying to touch its trunk. Tree justice. You know you've hit the big time when parts of your school's campus can murder you.",
        'image_url': 'https://ugc.reveliststatic.com/gen/full/2016/04/27/14/d4/e5/poaz7m4zcw39.gif'
    },
    {
        'name': 'Hexxus, "Fern Gully"',
        'description': "Okay, technically Hexxus is an evil (and confusingly sexy) oil spirit who starts the movie trapped in a tree and then ends the movie trapped in a different tree — but both trees are just incredible looking in terms of design. Plus the whole film is about how you shouldn't cut down trees, and implying that some of them are evil is a pretty decent deterrent.",
        'image_url': 'https://ugc.reveliststatic.com/gen/constrain/800/800/80/2016/04/27/14/8i/xh/povgpkhmsk39.jpg'
    },
    {
        'name': 'The Keebler Elf Tree',
        'description': 'Can any of these other trees give you cookies? Definitely not.',
        'image_url': 'https://ugc.reveliststatic.com/gen/constrain/800/800/80/2016/04/27/14/72/x3/po5rzeca8s39.jpg'
    },
    {
        'name': 'The Tree of Souls, "Avatar"',
        'description': "Say what you want about whether any of the characters from James Cameron's 2009 game-changer are really all that memorable, but that gorgeous tree the Na'Vi worship certainly is.",
        'image_url': 'https://ugc.reveliststatic.com/gen/full/2016/04/27/14/5b/k5/pou6flr8so39.gif'
    },
    {
        'name': 'The Weirwood, "Game Of Thrones"',
        'description': "We don't even really know what's going on with the Weirwood — are they the old gods? Or are they just relics from an old religion that isn't gonna matter much when the Whitewalkers come blazing through the North? Either way, they're pretty dang fascinating once you actually read into their history.",
        'image_url': 'https://ugc.reveliststatic.com/gen/full/2016/04/27/14/5z/ue/po610uplwk39.gif'
    },
    {
        'name': 'Treebeard, "The Lord Of The Rings" trilogy',
        'description': "He's the big daddy in the Forest of Fangorn, the eldest of the Ents – and a hoot at parties. Or perhaps not: Treebeard speaks in a deliberately slow manner, is careful not to rush anything (motto: \"Do not be hasty\") and almost bores Pippin and Merry to tears during their lengthy encounter. Despite the fact that he and his Ent brothers played their part in the eventual downfall of Saruman and the Orc armies, he sounds like the tree equivalent of the kind of person you get stuck behind walking through the London Underground. And yet we love him so!",
        'image_url': 'https://oyster.ignimgs.com/wordpress/stg.ign.com/2014/07/treebeard-720x405.jpg'
    },
    {
        'name': 'Groot, "Guardians Of The Galaxy"',
        'description': "Actually, Groot isn't a tree at all – he's a sentient, tree-like creature from outer space who is (in the comics) the monarch of Planet X, and not just somewhere for dogs to wee up in the park. Capable of saying just three words – \"I am Groot\" – he's not the most chatty of trees, but he puts more inflection into those three words than you might think. You see, Groot is actually super-intelligent and something of an expert in quasi-dimensional super-positional engineering – it's just that Groot's wooden larynx renders the subtleties of his speech void to human ears. Also, he's quite nice to sit under when it's sunny out. Of course, we still mourn the original Groot, but Baby Groot took his place in Guardians Vol. 2, followed by Teen Groot!",
        'image_url': 'https://ugc.reveliststatic.com/gen/full/2016/04/27/14/2s/on/poxm8pbhog39.gif'
    },
    {
        'name': 'Grandmother Willow, "Pocahontas"',
        'description': "Face made of green bark and with hollow black eyes, old lady Willow looks like something Guillermo del Toro might sketch after a particularly bad cheese nightmare, but in the Disney universe, a tree with a face – and a song to sing! - is par for the course. Grandmother Willow tells Pocahontas to listen to her heart and sets her on her path, but we would not recommend asking real trees for advice unless you want to become known as a \"colourful character\" in your local paper.",
        'image_url': 'https://ugc.reveliststatic.com/gen/full/2016/04/27/14/5s/um/pop8qxdz8k39.gif'
    },
    {
        'name': 'Apple Trees from Wizard of Oz',
        'description': "There's plenty nightmarish about The Wizard of Oz, but the concept of talking trees who vocally object when you pluck their fruit as Dorothy does is quite distressing. Does this cause them physical pain? They certainly seem very put out. \"How would you like someone to come along and pick something off of you?\" one tree asks Dorothy. Do all trees secretly feel this way? When trees lose their leaves in Autumn, is that them going bald every year? How horrible. In any case, Scarecrow intervenes before it all gets a bit Evil Dead.",
        'image_url': 'https://oyster.ignimgs.com/wordpress/stg.ign.com/2014/07/wizard-of-oz-720x540.jpg'
    },
    {
        'name': 'Sandbox Tree',
        'description': 'Considered to be one of the most dangerous trees in the world. It can grow up to 130 feet and its trunk is covered in cone-shaped spikes. What is really scary about this tree is the seeds it produces. The seeds look like small pumpkins and when they harden and mature, they become time bombs! Once fully mature, the seeds will explode and shoot out seeds at speeds up to 150 miles per hour and at distances of 60 feet! This is pretty dangerous for any creature to be in the trajectory! Not only that, but the tree is poisonous too! The Sandbox tree is native to South America and the Amazonian Rainforest.',
        'image_url': 'https://cdn.shopify.com/s/files/1/0027/0224/6000/files/Hura_crepitans_03_large.jpg'
    },
    {
        'name': "Dragon's Blood Tree",
        'description': 'In the Canary Islands of north-west Africa, there is a type of tree that holds a mysterious and legendary past. On the island of Tenerife, local legend has it that once a dragon dies, it becomes a tree, leading to these specimens becoming considered as living fossils in folklore. Standing at 50 feet tall, the impressive Dragon’s Blood tree gets it’s name from the red sap that can be obtained from the bark once cut. This was once used for the mummification process by the Guanche people of the island for centuries, but has now found its use in dye and medicine.',
        'image_url': 'https://www.internationaltimber.com/wp-content/uploads/2019/02/tree6-600x393.jpg'
    },
    {
        'name': 'Rainbow Eucalyptus',
        'description': 'This tall tree is known for its multi-coloured bark. It is native to Indonesia, the Philipines and Papua New Guinea. The bark of the rainbow eucalyptus sheds periodically and at different times of the year on the tree, revealing red, blue, purple and orange bark. It is also the only known Eucalyptus that grows natively in the Northern Hemisphere.',
        'image_url': 'https://cdn1.matadornetwork.com/blogs/1/2014/09/Rainbow-eucalyptus-in-Kauai-Hawaii.jpg'
    },
    {
        'name': 'Crooked Forest of Gryfino',
        'description': 'In a remote forest located near the town of Gryfino, West Poland, are 400 oddly shaped trees. Thought to have been curved from mechanical intervention, the purpose of these trees is not known. Many have speculated that they would have been used for bentwood furniture or even ribs for boat hulls. The outbreak of World War II in Poland in 1939, however, meant whoever was growing them had to stop and thus they became one of history’s great arboreal mysteries.',
        'image_url': 'https://www.internationaltimber.com/wp-content/uploads/2019/02/tree3-600x468.jpg'
    },
    {
        'name': 'Baobab tree, Africa',
        'description': 'The Baobab tree is one of the strangest looking trees. It has a very tall, huge trunk that holds an umbrella canopy. It is one of the few plants that can survive living on the African savannah. During the rainy season, the trunk becomes a reservoir of water. Then, during the driest part of the year, the tree produces a nutrient dense fruit. For this reason it is known as "The Tree of Life."',
        'image_url': 'https://cdn.shopify.com/s/files/1/2341/3995/files/graphic-node-yPSbirjJWzs-unsplash_2048x2048.jpg'
    },
    {
        'name': 'Silk Cotton Tree in Cambodia',
        'description': 'Named for the fibrous tuft produced by its seed pods, this species of trees is famous for the way they have grown into and around the Temple of Ta Prohm. While the trunks of the trees rise high above the temple, the snake-like roots coil around the ruins of the temple. These trees are some of the largest in the world. The oldest known Silk Cotton Tree can be found in Miami, Florida. It is estimated to be 200 years old.',
        'image_url': 'https://s3-us-west-2.amazonaws.com/media-tentree-com/wp-content/uploads/2017/04/White_Silk_Cotton_Tree_Lalbagh_Botanical_Garden_Bangalore-500x281.jpg'
    },
    {
        'name': 'Angel oak tree, South Carolina',
        'description': 'The famous Angel Oak tree — named not after the fact that it looks like Guillermo del Toro’s conception of the Angel of Death from Hellboy 2, but after its owners’ surname — is around 1,500 years old, growing just outside of Charleston.',
        'image_url': 'https://cdn1.matadornetwork.com/blogs/1/2014/09/Angel-Oak-Tree-South-Carolina.jpg'
    },
    {
        'name': 'Giant sequoias, California',
        'description': '',
        'image_url': 'https://cdn1.matadornetwork.com/blogs/1/2014/06/General-Sherman-in-Sequoia-National-Park-California.jpg'
    }
]


class TreesResource(Resource):
    """
    this Resource file is for our /users endpoints which don't require
    a resource ID in the URI path
    """
    def get(self, *args, **kwargs):
        return {
            'success': True,
            'count': len(TREES),
            'trees': TREES
        }, 200


class WhichTreeResource(Resource):
    def post(self, *args, **kwargs):
        data = json.loads(request.data)

        if 'name' not in data or bleach.clean(data['name'].strip()) == '':
            return {
                'success': False,
                'error': 'missing or empty "name" parameter'
            }, 400

        formatted_name = "".join(data['name'].lower().split())
        name_length = len(formatted_name)
        print(f'formatted_name >>{formatted_name}<<')
        name_sum = sum([ord(x) for x in formatted_name])
        print('len', name_length, 'sum', name_sum)
        tree = TREES[name_sum*name_length % len(TREES)]

        print('tree', tree)
        return {
            'success': True,
            'result': tree
        }, 200

    #     user, errors = self._create_user()
    #     if user is not None:
    #         user_payload = _user_payload(user)
    #         user_payload['success'] = True
    #         return user_payload, 201
    #     else:
    #         return {
    #             'success': False,
    #             'error': 400,
    #             'errors': errors
    #         }, 400
    #
    #
    #     proceed, username, errors = _validate_field(
    #         data, 'username', proceed, errors, missing_okay=True)
    #     proceed, email, errors = _validate_field(
    #         data, 'email', proceed, errors, missing_okay=True)
    #
    #     if not proceed:
    #         return {
    #             'success': False,
    #             'error': 400,
    #             'errors': errors
    #         }, 400
    #
    #     if username and len(username.strip()) > 0:
    #         user.username = username
    #     if email:
    #         user.email = email
    #     user.update()
    #
    #     user_payload = _user_payload(user)
    #     user_payload['success'] = True
    #     return user_payload, 200

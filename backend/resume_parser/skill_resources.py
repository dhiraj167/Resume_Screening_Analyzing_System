"""
Skill Gap Learning Recommendations
Maps missing skills to curated learning resources (YouTube, Coursera, docs).
"""

LEARNING_RESOURCES = {
    'python': {
        'youtube': 'https://www.youtube.com/watch?v=_uQrJ0TkZlc',
        'coursera': 'https://www.coursera.org/learn/python',
        'docs': 'https://docs.python.org/3/',
        'github': 'https://github.com/trekhleb/learn-python',
    },
    'machine learning': {
        'youtube': 'https://www.youtube.com/watch?v=GwIo3gDZCVQ',
        'coursera': 'https://www.coursera.org/learn/machine-learning',
        'docs': 'https://scikit-learn.org/stable/tutorial/',
        'github': 'https://github.com/ageron/handson-ml3',
    },
    'deep learning': {
        'youtube': 'https://www.youtube.com/watch?v=aircAruvnKk',
        'coursera': 'https://www.coursera.org/specializations/deep-learning',
        'docs': 'https://www.deeplearningbook.org/',
        'github': 'https://github.com/fastai/fastai',
    },
    'tensorflow': {
        'youtube': 'https://www.youtube.com/watch?v=tPYj3fFJGjk',
        'coursera': 'https://www.coursera.org/learn/introduction-tensorflow',
        'docs': 'https://www.tensorflow.org/tutorials',
        'github': 'https://github.com/tensorflow/tensorflow',
    },
    'pytorch': {
        'youtube': 'https://www.youtube.com/watch?v=EMXfZB8FVUA',
        'coursera': 'https://www.coursera.org/learn/deep-neural-networks-with-pytorch',
        'docs': 'https://pytorch.org/tutorials/',
        'github': 'https://github.com/pytorch/pytorch',
    },
    'nlp': {
        'youtube': 'https://www.youtube.com/watch?v=CMrHM8a3hqw',
        'coursera': 'https://www.coursera.org/specializations/natural-language-processing',
        'docs': 'https://huggingface.co/course/chapter1',
        'github': 'https://github.com/huggingface/transformers',
    },
    'react': {
        'youtube': 'https://www.youtube.com/watch?v=bMknfKXIFA8',
        'coursera': 'https://www.coursera.org/learn/react-basics',
        'docs': 'https://react.dev/learn',
        'github': 'https://github.com/facebook/react',
    },
    'django': {
        'youtube': 'https://www.youtube.com/watch?v=PtQiiknWUcI',
        'coursera': 'https://www.coursera.org/learn/django-for-everybody',
        'docs': 'https://docs.djangoproject.com/en/stable/intro/tutorial01/',
        'github': 'https://github.com/django/django',
    },
    'docker': {
        'youtube': 'https://www.youtube.com/watch?v=fqMOX6JJhGo',
        'coursera': 'https://www.coursera.org/learn/docker-for-the-absolute-beginner',
        'docs': 'https://docs.docker.com/get-started/',
        'github': 'https://github.com/docker/docker-ce',
    },
    'sql': {
        'youtube': 'https://www.youtube.com/watch?v=HXV3zeQKqGY',
        'coursera': 'https://www.coursera.org/learn/sql-for-data-science',
        'docs': 'https://www.w3schools.com/sql/',
        'github': 'https://github.com/AndrejKarpathy/micrograd',
    },
    'aws': {
        'youtube': 'https://www.youtube.com/watch?v=ulprqHHWlng',
        'coursera': 'https://www.coursera.org/learn/aws-cloud-practitioner-essentials',
        'docs': 'https://docs.aws.amazon.com/getting-started/',
        'github': 'https://github.com/awsdocs',
    },
    'kubernetes': {
        'youtube': 'https://www.youtube.com/watch?v=X48VuDVv0do',
        'coursera': 'https://www.coursera.org/learn/google-kubernetes-engine',
        'docs': 'https://kubernetes.io/docs/tutorials/',
        'github': 'https://github.com/kubernetes/kubernetes',
    },
    'javascript': {
        'youtube': 'https://www.youtube.com/watch?v=PkZNo7MFNFg',
        'coursera': 'https://www.coursera.org/learn/javascript-basics',
        'docs': 'https://developer.mozilla.org/en-US/docs/Learn/JavaScript',
        'github': 'https://github.com/getify/You-Dont-Know-JS',
    },
    'computer vision': {
        'youtube': 'https://www.youtube.com/watch?v=u1loyDCoGbE',
        'coursera': 'https://www.coursera.org/learn/convolutional-neural-networks',
        'docs': 'https://docs.opencv.org/4.x/d9/df8/tutorial_root.html',
        'github': 'https://github.com/opencv/opencv',
    },
    'git': {
        'youtube': 'https://www.youtube.com/watch?v=RGOj5yH7evk',
        'coursera': 'https://www.coursera.org/learn/version-control-with-git',
        'docs': 'https://git-scm.com/doc',
        'github': 'https://github.com/progit/progit2',
    },
}


def get_learning_resources(skill: str) -> dict:
    """Get curated learning resources for a given skill."""
    skill_lower = skill.lower().strip()
    # Direct match
    if skill_lower in LEARNING_RESOURCES:
        return LEARNING_RESOURCES[skill_lower]
    # Partial match
    for key in LEARNING_RESOURCES:
        if key in skill_lower or skill_lower in key:
            return LEARNING_RESOURCES[key]
    # Generic fallback
    query = skill.replace(' ', '+')
    return {
        'youtube': f'https://www.youtube.com/results?search_query={query}+tutorial',
        'coursera': f'https://www.coursera.org/search?query={query}',
        'docs': f'https://www.google.com/search?q={query}+documentation',
        'github': f'https://github.com/search?q={query}&type=repositories',
    }


def get_skill_gap_resources(missing_skills: list) -> list:
    """Return learning resources for each missing skill."""
    result = []
    for skill in missing_skills[:10]:  # limit to top 10
        resources = get_learning_resources(skill)
        result.append({
            'skill': skill,
            'resources': resources,
        })
    return result

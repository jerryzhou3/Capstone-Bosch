#coding=utf-8

# Load CoQA by datasets.load_dataset

from __future__ import absolute_import, division, print_function
import json
import logging
import os
import datasets


MAX_Q_LEN = 100
YOUR_LOCAL_DOWNLOAD = '/root/sharedtask-dialdoc2021/data'



class CoQA(datasets.GeneratorBasedBuilder):
    'CoQA dataset'

    VERSION = datasets.Version('1.0.0')

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name='coqa_rc',
            version=VERSION,
            description='Load CoQA dataset for machine reading comprehension tasks',
        ),
    ]

    DEFAULT_CONFIG_NAME = 'coqa_rc'

    def _info(self):
        if self.config.name == 'coqa_rc':
            features = datasets.Features(
                {
                    'id': datasets.Value('string'),
                    'title': datasets.Value('string'),
                    'context': datasets.Value('string'),
                    'question': datasets.Value('string'),
                    'answers': datasets.features.Sequence(
                        {
                            'text': datasets.Value('string'),
                            'answer_start': datasets.Value('int32'),
                            # 'spans': datasets.features.Sequence(datasets.Value('string'))
                        }
                    ),
                    'domain': datasets.Value('string'),
                }
            )

        return datasets.DatasetInfo(
            description=None,
            features=features,
            supervised_keys=None,
            homepage=None,
            citation=None
        )
    
    
    def _split_generators(self, dl_manager):
        data_dir = YOUR_LOCAL_DOWNLOAD # point to local dir to avoid downloading the dataset again
        
        if self.config.name == 'coqa_rc':
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.VALIDATION,
                    gen_kwargs={
                        'filepath': os.path.join(
                            data_dir, 'coqa/coqa-dev-v1.0.json'
                        ),
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={
                        'filepath': os.path.join(
                            data_dir, 'coqa/coqa-train-v1.0.json'
                        ),
                    },
                ),
            ]
        
    
    def _generate_examples(self, filepath):
        '''This function returns the examples in the raw (text) form.'''
        if self.config.name == 'coqa_rc':
            logging.info('generating examples from = %s', filepath)
            with open(filepath, encoding='utf-8') as f:
                dial_data = json.load(f)['data']
                for dial in dial_data:
                    all_prev_utterances = []
                    for idx, question in enumerate(dial['questions']):
                        all_prev_utterances.append(
                            #'\t{}: {}'.format('user', question['input_text'])
                            '<Q>{}</Q>'.format(question['input_text'])
                        )
                        
                        all_prev_question_str = ' '.join(
                                list(reversed(all_prev_utterances))[:1+2*idx]
                        ).strip()
                        
                        all_prev_question = ' '.join(all_prev_question_str.split()[:MAX_Q_LEN])
                        
                        id_ = '{}_{}_{}'.format(dial['id'], dial['name'], question['turn_id'])
                        
                        answer = [
                            {
                                'text': dial['answers'][idx]['span_text'],
                                'answer_start': dial['answers'][idx]['span_start'],
#                                 'answer_end': dial['answers'][idx]['span_end']
                            }
                        ]
                        
                        qa = {
                                'id': id_, # For subtask1, the id should be this format.
                                'title': dial['filename'],
                                'context': dial['story'],
                                'question': all_prev_question,
                               # 'question': question['input_text'],
                                'answers': answer,  # For subtask1, 'answers' contains the grounding annotations for evaluation.
                                'domain': dial['source'],
                            }
                        
                        all_prev_utterances.append(
                            '<A>{}</A>'.format(dial['answers'][idx]['input_text'])
                        )
                        
                        yield id_, qa

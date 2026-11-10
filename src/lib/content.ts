import yaml from 'yaml';
import organisersYaml from '../data/organisers.yaml?raw';
import faqYaml from '../data/faq.yaml?raw';

export interface Person {
  name: string;
  url?: string;
  photo?: string;
}
export interface Team {
  institution: string;
  country: string;
  url?: string;
  people: Person[];
}
export interface FaqItem {
  q: string;
  a: string;
}

function parse<T>(text: string): T {
  return yaml.parse(text) as T;
}

export function getOrganisers(): Team[] {
  return parse<{ teams: Team[] }>(organisersYaml).teams;
}

export function getFaq(): FaqItem[] {
  return parse<FaqItem[]>(faqYaml);
}
